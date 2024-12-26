from .abcnode import AbstractNode
from abc import ABC
import pygame


class AbstractPhysicalNode(AbstractNode, ABC):

	def __init__(self, name, pos, size, scene, parent, controller):
		super().__init__(name, scene, parent, controller)
		self._rect = pygame.Rect(pos, size)
		self._update_global_rect = True
		self._global_rect = None

	def _convert_to_global(self, rect):
		self._update_global_rect = False
		if self._parent is not None:
			return self._parent._convert_to_global(
				pygame.Rect(
					(
						rect.x + self._parent._rect.x,
						rect.y + self._parent._rect.y
					),
					rect.size
				)
			)
		return rect.copy()

	def add_child(self, new_child):
		self._children.append(new_child)
		new_child._parent = self
		self.union_rect(new_child.get_local_rect())

	def reset_global_rect(self):
		self._update_global_rect = True

	def union_rect(self, new_rect):
		self._rect.union_ip(new_rect.move(self._rect.x, self._rect.y))
		self._update_global_rect = True

	def get_local_rect(self):
		return self._rect

	def get_global_rect(self):
		if not self._global_rect or self._update_global_rect:
			self._global_rect = self._convert_to_global(self._rect)
		return self._global_rect

	def remove_child(self, child_to_delete, recursive=False):
		super().remove_chidl(chidl_to_delete, recursive)
		self._update_global_rect = True

	def convert_point_to_global(self, point):
		if self._parent is not None:
			return self._parent.convert_point_to_global(
				(
					point[0] + self._parent._rect.x,
					point[1] + self._parent._rect.y
				)
			)
		return (
			point[0] + self._rect.x,
			point[1] + self._rect.y
		)

	def move(delta_x, delta_y):
		self._rect.move_ip(delta_x, delta_y)
		self._update_global_rect = True

	def move_to(new_pos_x, new_pos_y):
		self._rect.update((new_pos_x, new_pos_y), self._rect.size)
		self._update_global_rect = True
