from ..Application import AbstractFactory
from .drawingcontroller import DrawingController
from .simplefigure import SimpleFigure
from .node import Node


class DrawingFactory(AbstractFactory):

	def __init__(self, name, main_factory, factory_config):
		super().__init__(name, main_factory)
		self._surface = None
		self._controller = None
		self._simple_figure = None
		config = self.get_default_config()
		config.update(factory_config)

	@classmethod
	def init(cls, name, main_factory, config):
		f_drawing = cls(name, main_factory, config)
		f_drawing.logger.info('init drawing factory')

	def after_pygame_init(self):
		self.get_surface()

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
