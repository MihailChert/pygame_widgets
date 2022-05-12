import pygame


class Screen:
    COUNTER = 0

    def __init__(self, window, window_surface=None, surface_size=None):
        Screen.COUNTER += 1
        self.id = Screen.COUNTER
        self.parent = window
        if surface_size is not None:
            self.surface = window_surface
        self.elements = pygame.sprite.Group()
        self.active_elements = pygame.sprite.Group()

    def add_element(self, *element):
        self.elements.add(*element)
        self.active_elements.add(*element)

    def remove_element(self, *element):
        self.elements.remove(*element)
        self.active_elements.remove(*element)

    def is_screen_clear(self):
        return self.elements.empty()

    def after_add(self, parent, surface):
        self.parent = parent
        self.surface = surface

    def dispatch(self):
        self.parent.delete_screen(self.id, True)
        del self

    def leave(self):
        return

    def load(self):
        return

    def update(self):
        self.elements.update()

    def draw(self):
        self.elements.draw(self.surface)

    def get_parent(self):
        return self.parent
