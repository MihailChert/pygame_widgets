import pygame
from ..Application import AbstractFactory
from .drawingcontroller import DrawingController
from .simplefigure import SimpleFigure
from .node import Node


class DrawingFactory(AbstractFactory):

	def __init__(self, name, main_factory, factory_config):
		super().__init__(name, main_factory, factory_config)
		self._surface = None
		self._controller = None
		self._simple_figure = None
		config = self.get_default_config()
		config.update(factory_config)
		self.scenes = factory_config['scenes']
		self.main_scene = factory_config['main_scene']
		self.background_color = factory_config['background']

	def init(self, name, main_factory):
		super().init(name, main_factory)
		self.logger.info('init drawing factory')

	@classmethod
	def get_settings_loader(cls, source):
		config = {
			'scenes': cls.check_parameter(source.meta, 'scenes', True),
			'main_scene': cls.check_parameter(source.meta, 'main_scene', True),
			'background': cls.check_parameter(source.meta, 'background_color', default=pygame.Color('black'))
		}
		factory = cls(source.get_name(), source.depended, config)
		return factory

	def after_pygame_init(self):
		self.get_surface()
		for scene_name in self.scenes.keys():
			builder = self._main_factory.get_builder(self.scenes[scene_name])
			self.scenes[scene_name] = builder.build_sources(self.get_controller())

	@staticmethod
	def get_default_config():
		return {
			'background': 100
		}

	def get_controller(self):
		if self._controller is None:
			self._controller = DrawingController(self)
		return self._controller

	def draw_simple_figure(self):
		if self._simple_figure is None:
			self._simple_figure = SimpleFigure(self._surface)
		return self._simple_figure

	@staticmethod
	def get_node(name, pos, size, parent):
		return Node(name, pos, size, parent)

	def share_surface(self):
		self.draw_simple_figure()

	def get_surface(self):
		if self._surface is None:
			self._surface = self._main_factory.get_surface()
			self.share_surface()
		return self._surface
