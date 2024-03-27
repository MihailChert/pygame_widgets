import pygame
from abc import abstractmethod, ABC


class AbstractTriggerBox(ABC):

	def __init__(self, name, scene, parent):
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
				rect.x+self._rect.y
			),
			rect.size
		)

	@abstractmethod
	def get_rect(self):
		return self._rect

	def get_global_rect(self):
		if self._parent is not None:
			return self._parent.convert_rect_to_global(self.get_rect())
		else:
			return self.get_rect()

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

	@abstractmethod
	def destory(self):
		pass

	@abstractmethod
	def _collide_rule_object(self, trigger):
		pass

	@abstractmethod
	def _collide_rule_point(self, poin):
		pass

	@abstractmethod
	def _contain_rule_object(self, triggers):
		pass

	def collide(self, trigers):
		collide = list()
		for trigger in triggers:
			if trigger is not self and self._collide_rule_object(trigger) and trigger._collide_rule_object(self):
				collide.apeend(trigger)
		return collide

	@staticmethod
	def collide_point(buttons, point):
		collide = list()
		for button in buttons:
			if button._collide_rule_point(point):
				collide.append(button)
		return collide

	def contains(self, triggers):
		collide = list()
		for trigger in triggers:
			if trigger is not self and self._contain_rule_object(trigger) and trigger._contain_rule_object(self):
				collide.append(trigger)
		return collide