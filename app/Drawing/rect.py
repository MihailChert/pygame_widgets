import numpy
import pygame
from .abcfigure import AbstractFigure


class Rect(AbstractFigure):

	def __init__(self, name, parent, controller, scene, color, width, antialias, rect, align):
		super().__init__(name, parent, controller, scene, color, width, antialias)
		self._rect = rect
		self._align = align

	@classmethod
	def create_from_source(cls, source):
		if source.check_meta('rect') is not None:
			rect = pygame.Rect(*source.check_meta('rect'))
		elif source.check_meta('pos') is not None and source.check_meta('size') is not None:
			rect = pygame.Rect(source.check_meta('pos'), source.check_meta('size'))
		elif source.check_meta('x') is not None \
			and source.check_meta('y') is not None \
			and source.check_meta('width') is not None \
			and source.check_meta('height') is not None:
			
			rect = pygame.Rect(
				source.check_meta('x'),
				source.check_meta('y'),
				source.check_meta('width'),
				source.check_meta('height')
			)
		else:
			source.check_meta('rect or (pos, size) or (x, y, width, height)', True)
		try:
			scene = source.get_dependencies(0).get_content().get_scene()
		except (AttributeError, TypeError):
			scene = source.get_root().get_name()
		res = cls(
			source.get_name(),
			None,
			source.meta['controller'],
			scene,
			source.check_meta('color', default=[0, 0, 0]),
			source.check_meta('line_width', default=0),
			source.check_meta('antialias', default=False),
			rect,
			source.check_meta('align', default=0)
		)
		res.connect_events_from_source(source)
		return res

	def get_rect(self):
		if self._align:
			points = self.get_points()
			width = numpy.max(points[:, 0]) - numpy.min(points[:, 0])
			height = numpy.max(points[:, 1]) - numpy.min(points[:, 1])
			return pygame.Rect(
				(
					points[:, 0].min(),
					points[:, 1].min()
				),
				(width, height)
			)
		else:
			return self._rect

	def get_align(self):
		return self._align

	def get_points(self):
		rect = self._rect
		points = numpy.array(
			[
				rect.topleft,
				rect.topright,
				rect.bottomright,
				rect.bottomleft
			],
			numpy.int32
			)
		points = numpy.array(
			[
				((points[:, 0] - rect.centerx) * numpy.cos(self._align) - (points[:, 1] - rect.centery) * numpy.sin(self._align)) + rect.centerx,
				((points[:, 0] - rect.centerx) * numpy.sin(self._align) + (points[:, 1] - rect.centery) * numpy.cos(self._align)) + rect.centery
			],
			numpy.int32
		).transpose()
		return points

	def _get_global_points(self):
		parent = self._parent
		rect = self.get_rect()
		while parent is not None:
			parent_rect = parent.get_rect()
			rect.move_ip(parent_rect.x, parent_rect.y)
			parent = parent.get_parent()
		delta_pos = [rect.x - self.get_rect().x, rect.y - self.get_rect().y]
		return self.get_points() + numpy.array([delta_pos], numpy.int32)

	def move(self, delta_x=0, delta_y=0):
		self._controller.calc_update_zone(self.get_global_rect())
		self._rect.move_ip(delta_x, delta_y)
		self._controller.calc_update_zone(self.get_global_rect())


	def resize(self, delta_width=0, delta_height=0):
		if delta_width > 0:
			self._rect.width += delta_width
		if delta_height > 0:
			self._rect.height += delta_height
		self._controller.calc_update_zone(self.get_global_rect())
		if delta_width < 0:
			self._rect.width += delta_width
		if delta_height < 0:
			self._rect.height += delta_height

	def update_pos(self, x=None, y=None):
		self.move(x-self._rect.x, y-self._rect.y)

	def rotate(self, align, radians=False):
		self._controller.calc_update_zone(self.get_global_rect())
		if not radians:
			align = self.deg2rad(align)
		self._align = (self._align+align) % (numpy.pi / 2)
		self._controller.calc_update_zone(self.get_global_rect())

	def reset_align(self):
		self._align = 0

	def _draw(self):
		if self._align:
			pygame.draw.polygon(
				self._controller.get_app().get_screen(),
				self.color,
				self._get_global_points(),
				self.width
			)
		else:
			pygame.draw.rect(
				self._controller.get_app().get_screen(),
				self.color,
				self.get_global_rect(),
				self.width
			)
