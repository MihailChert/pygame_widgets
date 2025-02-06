import numpy
import pygame
from .abcfigure import AbstractFigure


class Circle(AbstractFigure):

	def __init__(self, name, parent, controller, scene, color, width, center, radius):
		super().__init__(name, parent, controller, scene, color, width, False)
		self._radius = abs(radius)
		self._rect = pygame.Rect(numpy.array(center, numpy.int32)-radius, [self._radius*2]*2)

	def get_radius(self):
		return self._radius

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
			source.check_meta('line_width', default=0),
			source.check_meta('pos', True),
			source.check_meta('radius', True)
		)
		res.connect_events_from_source(source)
		return res

	def get_rect(self):
		return self._rect

	def move(self, delta_x=0, delta_y=0):
		self._controller.calc_update_zone(self.__rect)
		self._rect.move_ip(delta_x, delta_y)
		self._controller.calc_update_zone(self._rect)

	def resize(self, delta_radius):
		if delta_raidus > 0:
			rect_scale = (self._radius+delta_radius) / self._radius
			self._rect.scale_by(rect_scale, rect_scale)
		self._controller.calc_update_zone(self.__rect)
		if delta_raidus < 0:
			rect_scale = abs((self._radius+delta_radius) / self._radius)
			self._rect.scale_by(rect_scale, rect_scale)
		self._raidus += delta_radius

	def update_pos(self, x=None, y=None):
		self.move(x-self._center[0], y-self._center[1])

	def rotate(self):
		return

	def _draw(self):
		pygame.draw.circle(self._controller.get_app().get_screen(), self.color, self.get_global_rect().center, self._radius, self.width)