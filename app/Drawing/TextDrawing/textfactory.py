import pygame
from ...Application import AbstractFactory


class TextFactory(AbstractFactory):

	def __init__(self, name, main_factory):
		super().__init__(name, main_factory)

	@classmethod
	def init(cls, name, main_factory, app_config):
		pygame.font.init()
		cls(name, main_factory)

	def after_pygame_init(self):
		pass

	@staticmethod
	def get_default_config():
		return {}

	def get_controller(self):
		return self._main_factory.factories['drawing'].get_controller()

	def get_drawing_factory(self):
		return self._main_factory.factories['drawing']

	def get_text_loader(self, source):
		pass

	@staticmethod
	def get_font(font, font_size):
		return pygame.font.Font(font, font_size)
