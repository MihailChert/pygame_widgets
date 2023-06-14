import pygame
import math
import sys


class SimpleFigure:

	def __init__(self, dr_surface):
		self._surface = dr_surface
		self._back_color = None

	def set_background(self, color):
		self._back_color = color

	def set_surface(self, surface):
		self._surface = surface

	def rect(self, color, rect_points, width=0, border_radius=None):
		"""
		Parameters
		----------
		color: int, list, tuple, pygame.Color
		rect_points: list, tuple, pygame.Rect
		width: int
		border_radius: int, list, tuple
			[top_left, top_right, bottom_left, bottom_right]

		Returns
		-------
		pygame.Rect
		"""
		if isinstance(border_radius, int) or isinstance(border_radius, (list, tuple)) and len(border_radius) == 1:
			return pygame.draw.rect(self._surface, color, rect_points, border_radius=border_radius, width=width)
		else:
			b_r = self.parse_border(border_radius)
			return pygame.draw.rect(self._surface, color, rect_points, width, 0, b_r[0], b_r[1], b_r[2], b_r[3])

	def rot_rect(self, color, rect_points, width=0, antialiased=False):
		points = []
		start_point = rect_points[0]
		for point in rect_points:
			if start_point is point:
				continue
			points.append((start_point, point))
			start_point = point
		if antialiased:
			return self.lines(color, points, True, width, True)
		else:
			return pygame.draw.polygon(self._surface, color, points, width)

	def polygon(self, color, poly_points, width=0):
		return pygame.draw.polygon(self._surface, color, poly_points, width)

	def circle(self, color, center_pos, radius, width=0, top_left=False, top_right=False, bottom_left=False, bottom_right=False):
		return pygame.draw.circle(self._surface, color, center_pos, radius, width, top_right, top_left, bottom_left, bottom_right)

	def ellipse(self, color, ellipse_rect=None, h_radius=0, w_radius=0, el_center=None, width=0):
		if ellipse_rect is None:
			left = el_center[0] - w_radius // 2
			top = el_center[1] - h_radius // 2
			ellipse_rect = pygame.Rect(left, top, w_radius, h_radius)
		return pygame.draw.ellipse(self._surface, color, ellipse_rect, width)

	def arc(self, color, start_angle, stop_angle, ellipse_rect=None, h_radius=0, w_radius=0, el_center=None, is_degr=False, width=0):
		if ellipse_rect is None:
			left = el_center[0] - w_radius // 2
			top = el_center[1] - h_radius // 2
			ellipse_rect = pygame.Rect(left, top, w_radius, h_radius)
		if is_degr:
			start_angle = math.radians(start_angle)
			stop_angle = math.radians(stop_angle)
		return pygame.draw.arc(self._surface, color, ellipse_rect, start_angle, stop_angle, width)

	def line(self, color, start_pos, end_pos, width=0, antialiased=False):
		if antialiased:
			return pygame.draw.aaline(self._surface, color, start_pos, end_pos)
		else:
			return pygame.draw.line(self._surface, color, start_pos, end_pos, width)

	def lines(self, color, points, closed, width=0, antialiased=False):
		if antialiased:
			return pygame.draw.aalines(self._surface, color, closed, points)
		else:
			return pygame.draw.lines(self._surface, color, closed, points, width)

	@staticmethod
	def parse_border(border_r):
		"""
		Parameters
		----------
		border_r

		Returns
		-------
		list[top_left, top_right, bottom_left, bottom_right]
		"""

		if isinstance(border_r, (list, tuple)):
			if sys.version_info >= (3, 10):
				match len(border_r):
					case 2:
						return [border_r[0], border_r[0], border_r[1], border_r[1]]
					case 4:
						return border_r
					case _:
						raise ValueError('Incorrect border length: ' + len(border_r))
			else:
				if len(border_r) == 2:
					return [border_r[0], border_r[0], border_r[1], border_r[1]]
				elif len(border_r) == 4:
					return border_r
				else:
					raise ValueError('Incorrect border length: ' + len(border_r))
		if isinstance(border_r, dict):
			pass  # TODO: parser for dict border

	def draw_background(self, color):
		self._surface.fill(color)
