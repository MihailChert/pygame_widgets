import pygame
from ...Application import AbstractController


class TextController(AbstractController):

    def __init__(self, factory):
        super().__init__(factory)
        self._event_id = self.create_event_id()

    def destroy(self, event):
        pygame.font.quit()

    def get_text_loader(self, source):
        source.meta['controller'] = self
        cls = None
        for dependence in source.get_dependencies():
            if dependence.get_name() == source.get_source():
                cls = dependence.get_content()
                break
        return cls.create_from_source(source)

    def find_object(self, needle_object):
        pass
