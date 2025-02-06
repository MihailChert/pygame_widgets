import numpy
import pygame
from .abcfigure import AbstractFigure


class Polygone(AbstractFigure):

	def __init__(self, name, parent, controller, scene, color, width, points, align):
		super().__init__(name, parent, controller, scene, color, width, False)
		self._align = align
		self.__rect = None
		self._points = numpy.array(points, numpy.int32)
		if len(self._points.shape) != 2 and 2 not in self._points.shape:
			raise ValueError('Unexpected points strycture. Array shape mast be (2,n) or (n,2), given: ' + self._points.shape)
		if self._points.shape[0] == 2:
			self._points = self._points.transpose()

	@classmethod
	def create_from_source(cls, source):
		try:
			scene = source.get_dependencies(0).get_content().get_scene()
		except(AttributeError, TypeError):
			scene = source.get_root().get_name()
		res = cls(
			source.get_name(),
			None,
			source.meta['controller'],
			scene,
			source.check_meta('color', default=pygame.Color('black')),
			source.check_meta('line_width' default=0),
			source.check_meta('points', True)
		)
		return res

	def get_rect(self):
		if self.__rect is None:
			self.__rect = pygame.Rect(
				(self._points[:, 0].min(), self._points[:, 1].max()),
				(
					self._points[:, 0].max() - self._points[:,0].min(),
					self._points[:,1].max() - self._points[:,1].min()
				)
			)
		return self.__rect

	def get_align(self):
		return self._align

	def move(self, delta_x=0, delta_y=0):
		self._controller.calc_update_zone(self.get_rect())
		self.__rect = None
		self._points = self._points + numpy.array([[delta_x, delta_y]])
		self._controller.calc_update_zone(self.get_rect())

	def resize(self, delta_width=0, delta_height=0):
		self._controller.calc_update_zone(self.get_rect())


		self.__rect = None
		self._controller.calc_update_zone(self.get_rect())