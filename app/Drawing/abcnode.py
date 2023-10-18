import pygame
from abc import ABC, abstractmethod


class AbstractNode(ABC):

	def __init__(self, name, pos, size, scene, parent):
		self._rect = pygame.Rect(pos, size)
		self._parent = parent
		self._scene = scene
		if name is None:
			self._name = 'Node' + id(self)
		else:
			self._name = name

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

	def get_rect(self):
		return self._rect

	def get_global_rect(self):
		if self._parent is not None:
			return self._parent.convert_rect_to_global(self._rect)
		else:
			return self._rect

	def get_name(self):
		return self._name

	def get_parent(self):
		return self._parent

	def get_scene(self):
		return self._scene

	def convert_point_to_global(self, point):
		if self._parent is not None:
			return self._parent.convert_point_to_global(
				(
					point[0] + self._rect.x,
					point[1] + self._rect.y
				)
			)
		return point[0] + self._rect.x, point[1] + self._rect.y

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
			ret_list.append((point[0] + self._rect.x, point[1] + self._rect.y))
		if self._parent is not None:
			return self._parent.convert_points_to_global(ret_list)
		return ret_list

	def on_scene(self, scene_name):
		return self._scene == scene_name

	@abstractmethod
	def destroy(self):
		pass

	@abstractmethod
	def _draw(self):
		pass
