import pygame
from ...Application import AbstractController


class TextController(AbstractController):

    def __init__(self, factory):
        super().__init__(factory)
        self.__drawing_controller = factory.get_drawing_factory().get_controller()
        self._event_id = self.__drawing_controller.get_event_id()

    def add_listener_to(self, listened_method, handler):
        if listened_method == 'empty_method':
            self.logger.error('add listener to handler method')
            raise ValueError('\'empty_method\' con\'t have any listeners')
        self.__drawing_controller.add_listener_to('text_'+listened_method, handler)

    def destroy(self, event):
        pygame.font.quit()

    def create_event(self, method, event_attrs):
        method = 'text_' + method
        self.__drawing_controller.create_event(method, event_attrs)

    def find_object(self, needle_object):
        pass
