import pygame
from ...Application import AbstractFactory
from .textcontroller import TextController


class TextFactory(AbstractFactory):

    def __init__(self, name, main_factory, config):
        super().__init__(name, main_factory)
        self._controller = None

    @classmethod
    def init(cls, name, main_factory, config):
        pygame.font.init()
        text = cls(name, main_factory, config)
        text.logger.info('init text factory')

    @staticmethod
    def get_default_config():
        return {}

    def get_controller(self):
        if self._controller is None:
            self._controller = TextController(self)
        return self._controller

    def get_drawing_factory(self):
        return self._main_factory.factories['drawing']
