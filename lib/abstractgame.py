import sys
import abc
import pygame

from typing import Union, Optional, Iterable

from .event import Event
from .screen import Screen


class AbstractGame(abc.ABC):

    @abc.abstractmethod
    def __init__(self, size, fps=0, is_font=False, is_music=False, is_resizable=False, is_full_screen=False, flags=0):
        if is_font:
            pygame.font.init()
        if is_music:
            pygame.mixer.init()
        pygame.init()
        flags = flags | (pygame.RESIZABLE if is_resizable else 0) | (pygame.FULLSCREEN if is_full_screen else 0)
        self.window = pygame.display.set_mode(size, flags)
        self.active_screen = Screen(self, self.window)
        self.screens = [self.active_screen]
        self.clock = pygame.time.Clock()
        self.fps = fps

    def add_screen(self, new_screen):
        if not isinstance(new_screen, Screen):
            raise RuntimeError('It is not a screen.')
        self.screens.append(new_screen)
        new_screen.after_add(self, self.window)

    def delete_screen(self, screen_id: Union[int, Iterable], is_from_dispatch=False):
        screen_iter = 0
        for screen in reversed(self.screens):
            if isinstance(screen_id, int) and screen_id == screen.id:
                self.screens.pop(len(self.screens) - screen_iter - 1)
                if not is_from_dispatch:
                    del screen
                break
            if isinstance(screen_id, Iterable) and screen_id in screen_id:
                self.screens.pop(len(self.screens) - screen_iter - 1)
                if not is_from_dispatch:
                    del screen
                continue
            screen_iter += 1

    def change_screen(self, screen_id):
        for screen in self.screens:
            if screen_id == screen.id:
                self.active_screen.leave()
                self.active_screen = screen
                screen.load()
                break
        else:
            raise RuntimeError(f'Cant find screen. Add the screen with id = {screen_id}.')

    def blocked_event_type(self, types):
        for event_type in types:
            if isinstance(event_type, (tuple, list)):
                Event.block_event(event_type[-1])
            elif isinstance(event_type, int):
                pygame.event.set_blocked(event_type)
            else:
                raise ValueError(f'Event type "{event_type}" must be int or tuple if it custom event.')

    def allove_event_type(self, types):
        for event_type in types:
            if isinstance(event_type, (tuple, list)):
                Event.allow_event(event_type[-1])
            elif isinstance(event_type, int):
                pygame.event.set_allowed(event_type)
            else:
                raise ValueError(f'Event type "{event_type}" must be int or tuple if it custom event.')

    @abc.abstractmethod
    def window_event(self):
        return

    @abc.abstractmethod
    def mouse_event(self, events):
        return

    @abc.abstractmethod
    def key_event(self, events):
        return

    @abc.abstractmethod
    def custom_event(self, events):
        return

    def before_quit(self):
        return

    def update(self):
        self.active_screen.update()

    def draw(self):
        self.active_screen.draw()

    def run(self):
        while True:
            self.clock.tick(self.fps)
            if pygame.event.peek(pygame.QUIT):
                self.before_quit()
                pygame.quit()
                sys.exit()
            if not pygame.event.get_blocked((pygame.MOUSEMOTION, pygame.MULTIGESTURE)):
                self.mouse_event(
                                pygame.event.get(
                                    [
                                        pygame.MOUSEMOTION,
                                        pygame.MOUSEBUTTONUP,
                                        pygame.MOUSEBUTTONDOWN,
                                        pygame.MOUSEWHEEL,
                                        pygame.MULTIGESTURE
                                    ]
                                )
                            )
            if not pygame.event.get_blocked(pygame.KEYDOWN) and not pygame.event.get_blocked(pygame.KEYUP):
                self.key_event(
                                pygame.event.get(
                                    [
                                        pygame.KEYDOWN,
                                        pygame.KEYUP
                                    ]
                                )
                            )
            if not pygame.event.get_blocked(Event.TYPE):
                self.custom_event(pygame.event.get(Event.TYPE))
            pygame.event.clear()

            self.update()

            self.draw()
