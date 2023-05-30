from pygame import Color
from ..Application import AbstractFactory
from .drawingcontroller import DrawingController
from .simplefigure import SimpleFigure


class DrawingFactory(AbstractFactory):

	def __init__(self, name, app, main_factory):
		super().__init__(self, name, app, main_factory)
		self._surface = None
		self._controller = None
		self._simple_figure = None
		self._background = None

	def init(self):
		self.logger.info('init drawing factory')

	def set_background(self, background):
		if isinstance(background, (int, list, tuple, Color)):
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
			self._main_factory.get_surface()
		return self._surface

	def fill_background(self):
		self._background.draw_background()
