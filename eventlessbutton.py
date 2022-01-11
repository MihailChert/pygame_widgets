from typing import Union, Optional, Any, Tuple, List, Callable

import pygame

from label import Label
from modules import Padding, Margin, SizeRange


class EventlessButton(Label):
    COUNTER = 0

    def __init__(
            self,
            parent,
            pos: Tuple[int, int],
            font: Optional[Tuple[str, int, pygame.Color]],
            text: str,
            background: Any,
            text_align: str,
            transparency: bool = False,
            rect_size: Union[pygame.Rect, List[int], Tuple[int, int, int, int]] = None,
            size_range: SizeRange = None,
            padding: Padding = Padding(10),
            borders: Union[int, List[int], Tuple[int, ...]] = 2,
            border_color: Union[pygame.Color, Tuple[int, int, int]] = (255, 255, 255),
            margin: Margin = Margin(0),
            target: Optional[Callable] = None,
    ):
        super().__init__(
            parent,
            pos,
            font,
            text,
            background,
            text_align,
            transparency,
            rect_size,
            size_range,
            padding,
            borders,
            border_color,
            margin,
        )
        Label.COUNTER -= 1
        self._id = EventlessButton.COUNTER
        EventlessButton.COUNTER += 1
        self.name = type(self).__name__ + str(self._id)
        self.target = target
        self._pressed = False
        self.select = self.default_select
        self.unselect = self.default_unselect
        self._active_color = self.surface_color

    @property
    def ispressed(self):
        return self._pressed

    def default_select(self):
        pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
        self._active_color = pygame.Color(abs(self.surface_color[0] - 40),
                                          abs(self.surface_color[1] - 40),
                                          abs(self.surface_color[2] - 40))

    def default_unselect(self):
        pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)
        self._active_color = self.surface_color

    def check_press(self, mouse_event, change_curr=False):
        if self.client_rect.collidepoint(mouse_event.pos):
            self.select()
            if mouse_event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
                if self._pressed ^ (mouse_event.type == pygame.MOUSEBUTTONDOWN):
                    try:
                        self.target()
                    except TypeError as er:
                        if self.target is not None:
                            raise er
                self._pressed = mouse_event.type == pygame.MOUSEBUTTONDOWN
            return True
        if not change_curr:
            self.unselect()
        self._pressed = False
        return change_curr

    def draw_pressed(self):
        self.surface.set_alpha(200)
        try:
            self.parent.blit(self.surface, self.client_rect)
        except AttributeError:
            self.parent.surface.blit(self.surface, self.client_rect)
        self.surface.fill(self._active_color)
        self.draw_text()

    def draw_unpressed(self) -> None:
        """Summary"""
        self.surface.set_alpha(255)
        self.parent.blit(self.surface, self.client_rect)
        self.surface.fill(self._active_color)
        self.draw_text()

    def draw(self):
        if self._pressed:
            self.draw_pressed()
        else:
            self.draw_unpressed()
