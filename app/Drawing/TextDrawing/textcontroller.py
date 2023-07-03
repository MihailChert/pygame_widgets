import pygame
from ...Application import AbstractController


class TextController(AbstractController):

    def __init__(self, factory):
        super().__init__(factory)
        self.__drawing_controller = factory.get_drawing_factory().get_controller()
        self._event = self.__drawing_controller.get_event_id()

    def add_listener_to(self, listened_method, handler):
        if listened_method == 'empty_method':
            self.logger.error('add listener to handler method')
            raise ValueError('\'empty_method\' con\'t have any listeners')
        self.__drawing_controller.add_listener_to('text_'+listened_method, handler)

    def destroy(self, event):
        pygame.font.quit()