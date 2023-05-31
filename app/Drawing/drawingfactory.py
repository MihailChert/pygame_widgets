from pygame import Color
from ..Application import AbstractFactory
from .drawingcontroller import DrawingController
from .simplefigure import SimpleFigure


class DrawingFactory(AbstractFactory):

	def __init__(self, name, main_factory, factory_config):
		super().__init__(name, main_factory)
		self._surface = None
		self._controller = None
		self._simple_figure = None
		config = self.get_default_config()
		config.update(factory_config)
		self.set_background(config['background'])

	@classmethod
	def init(cls, name, main_factory, config):
		f_drawing = cls(name, main_factory, config)
		f_drawing.logger.info('init drawing factory')

	def after_pygame_init(self):
		self.get_surface()
		print(self._surface)

	@staticmethod
	def get_default_config():
		return {
			'background': 100
		}

	def set_background(self, background):
		if isinstance(background, (int, list, tuple, Color)):
			self._background = self.draw_simple_figure()
			self._simple_figure.set_background(Color(background))
		else:
			self._background = background

	def get_controller(self):
		if self._controller is None:
			self._controller = DrawingController(self)
		return self._controller

	def draw_simple_figure(self):
		if self._simple_figure is None:
			self._simple_figure = SimpleFigure(self._surface)
		return self._simple_figure

	def get_surface(self):
		if self._surface is None:
			self._surface = self._main_factory.get_surface()
			self._simple_figure.set_surface(self._surface)
		return self._surface

	def fill_background(self):
		self._background.draw_background()
