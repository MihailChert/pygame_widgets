import numpy
import pygame
from .abcfigure import AbstractFigure


class Line(AbstractFigure):

	def __init__(self, name, parent, controller, scene, color, width, antialias, start_pos, end_pos):
		super().__init__(name, parent, controller, scene, color, width, antialias)
		self._start_pos = numpt.array(start_pos, dtype=numpy.int32)
		self._end_pos = numpy.array(end_pos, dtype=numpy.int32)

	@classmethod
	def create_from_source(cls, source):
		start_pos = (0,0)
		if source.check_meta('start_pos') is not None:
			start_pos = source.check_meta('start_pos')
		else:
			start_pos[0] = source.check_meta('start_x')
			start_pos[1] = source.check_meta('start_y')
		end_pos = (0,0)
		if source.check_meta('end_pos') is not None:
			end_pos = source.check_meta('end_pos')
		else:
			end_pos[0] = source.check_meta('end_x')
			end_pos[1] = source.check_meta('end_y')
		scene = None
		try:
			scene = source.get_dependencies(0).get_content().get_scene()
		except(AttributeError, TypeError):
			scene = source.get_root().get_name()
		res = cls(
			source.get_name(),
			None,
			source.meta['controller'],
			scene,
			source.check_meta('color', default=[0,0,0]),
			source.check_meta('line_width', default=1),
			source.check_meta('antialias', default=False),
			start_pos,
			end_pos
		)
		res.connect_events_from_source(source)
		return res

	def get_rect(self):
		rect = pygame.Rect(
			min(self._start_pos[0], self._end_pos[0]),
			min(self._start_pos[1], self._end_pos[1]),
			abs(self._start_pos[0] - self._end_pos[0]),
			abs(self._start_pos[1] - self._end_pos[1])
		)
		return rect

	def get_points(self):
		return numpy.array([self._start_pos, self._end_pos], dtype=int32)

	def get_global_points(self):
		parent = self._parent
		rect = self.get_rect()
		while parent is not None:
			parent_rect = parent.get_rect()
			rect.move_ip(parent_rect.x, parent_rect.y)
			parent = parent.get_parent()
		delta_pos = [rect.x - self.get_rect().x, rect.y - self.get_rect().y]
		return (self._start_pos + delta_pos[0], self._end_pos + delta_pos[1])

	def _draw(self):
		points = self.get_global_points()
		pygame.draw.line(self._controller.get_app().get_screen(), self.color, points[0], points[1], self._width)