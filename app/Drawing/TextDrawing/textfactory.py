import pygame
from ...Application import AbstractFactory
from .textcontroller import TextController


class TextFactory(AbstractFactory):

	def __init__(self, name, main_factory, config):
		super().__init__(name, main_factory, config)
		self._controller = None

	def init(self, name, main_factory):
		pygame.font.init()
		super().init(name, main_factory)
		self.logger.info('init text factory')

	@classmethod
	def get_factory_loader(cls, source):
		factory = super(TextFactory, cls).get_factory_loader(source)
		return factory

	@staticmethod
	def get_default_config():
		return {}

	def after_pygame_init(self):
		pass

	def get_controller(self):
		if self._controller is None:
			self._controller = TextController(self)
		return self._controller

	def get_drawing_factory(self):
		return self._main_factory.factories['drawing']

	@staticmethod
	def get_font(font, font_size):
		return pygame.font.Font(font, font_size)

	def get_font_loader(self, source):
		pass
