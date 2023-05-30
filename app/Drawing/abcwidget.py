import pygame
from abc import ABC, abstractmethod


class AbstractWidget(ABC):

	def __init__(self, pos, size, parent):
		self._rect = pygame.Rect(pos, size)
		self._parent = parent

	def convert_rect_to_global(self, rect):
		if self._parent is not None:
			return self._parent.convert_rect_to_global(
				pygame.Rect(
					(
						rect.x+self._rect.x,
						rect.y+self._rect.y
					),
					rect.size
				)
			)
		return pygame.Rect(
			(
				rect.x+self._rect.x,
				rect.y+self._rect.y
			),
			rect.size
		)

	def convert_point_to_global(self, point):
		if self._parent is not None:
			return self._parent.convert_point_to_global(
				(
					point[0] + self._rect.x,
					point[1] + self._rect.y
				)
			)
		return point[0] + self._rect.x, point[1] + self._rect_y

	def convert_rects_to_global(self, rect_list):
		ret_list = []
		for rect in rect_list:
			rect = pygame.Rect((rect.x+self._rect.x, rect.y+self._rect.y), rect.size)
			rect_list.append(rect)
		if self._parent is not None:
			return self._parent.convert_rects_to_global(ret_list)
		return ret_list

	def convert_points_to_global(self, points_list):
		ret_list = []
		for point in points_list:
			ret_list.append(point[0] + self._rect.x, point[1] + self._rect.y)
		if self._parent is not None:
			return self._parent.convert_points_to_global(ret_list)
		return ret_list

	@abstractmethod
	def dispatch(self):
		pass

	@abstractmethod
	def draw(self, surface):
		pass
