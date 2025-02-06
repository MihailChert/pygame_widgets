import numpy
import pygame
from ..Aplication import AbstractPhysicalNode
from .abcfigure import AbstractFigure


class Rect(AbstractPhysicalNode):

	def __init__(self, name, pos, size, scene, parent, controller, color, bg_color, width, antialias, align):
		super().__init__(name, pos, size, scene, parent, controller, bg_color)
		self._align = align
		self._drawing_points = None
		self._color = color
		self._width = width
		self._antialias = antialias
		self._update_draw = True
		self._bg_color = bg_color
		self._recalculate_local_rect()

	def get_color(self):
		return self._color

	def set_color(self, new_color):
		self._color = new_color
		self._update_draw = True

	def get_width(self):
		return self._width

	def set_width(self, new_width):
		self._width = new_width
		self._update_draw = True

	def get_align(self):
		return self._align

	def set_align(self, new_align):
		self._align = new_align
		self._update_draw = True

	def get_antialias(self):
		return self._antialias

	def set_antialias(self, new_antialias):
		self._antialias = new_antialias
		self._update_draw = True

	def get_bg_color(self):
		return self._bg_color

	def set_bg_color(self, new_bg_color):
		self._bg_color = new_bg_color
		self._update_draw = True


	color = property(fget = get_color, fset = set_color)
	width = property(fget = get_width, fset = set_width)
	antialias = property(fget = get_antialias, fset = set_antialias)
	bg_color = property(fget = get_bg_color, fset = set_bg_color)
	align = property(fget = get_align, fset = set_align)


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
			rect.pos,
			rect.size,
			scene,
			None,
			source.meta['controller'],
			source.check_meta('color', default=[0, 0, 0]),
			source.check_meta('line_width', default=0),
			source.check_meta('antialias', default=False),
			source.check_meta('align', default=0)
		)
		res.connect_events_from_source(source)
		return res

	def _update_drawing_points(self):
		rect = rect = self._rect
		points = numpy.array(
			[
				rect.topleft,
				rect.topright,
				rect.bottomright,
				rect.bottomleft
			],
			numpy.int32
			)
		self._drawing_points = numpy.array(
			[
				((points[:, 0] - rect.centerx) * numpy.cos(self._align) - (points[:, 1] - rect.centery) * numpy.sin(self._align)) + rect.centerx,
				((points[:, 0] - rect.centerx) * numpy.sin(self._align) + (points[:, 1] - rect.centery) * numpy.cos(self._align)) + rect.centery
			],
			numpy.int32
		).transpose()

	def get_local_rect(self):
		x = numpy.min(self._drawing_points[:, 0])
		y = numpy.min(self._drawing_points[:, 1])
		self._rect = pygame.Rect(
			(x, y),
			(numpy.max(self._drawing_points[:, 0]) - x,
			numpy.max(self._drawing_points[:, 1]) - y)
		)

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
		super().move(delta_x, delta_y)
		self._update_draw = True

	def move_to(self, new_pos_x, new_pos_y):
		super().move_to(new_pos_x, new_pos_y)
		self._update_draw = True


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
		self._update_global_rect = True
		self._update_draw = True

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
			self._update_drawing_points()
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
