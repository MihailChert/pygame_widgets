import pygame
from .abctriggerbox import AbstractTriggerBox


class RectTriggerBox(AbstractTriggerBox):

	def __init__(self, name, scene, parent, shape, pos, size):
		self._rect = pygame.Rect(pos, size)
		super().__init__(name, scene, parent)

	def get_rect(self):
		return self._rect

	def destroy(self):
		del self._rect

	def _collide_rule_object(self, trigger):
		return self._rect.colliderect(trigger.get_rect())

	def _collide_rule_point(self, point):
		return self._rect.collidepoint(point)

	def _contain_rule_object(self, trigger):
		return self._rect.contains(trigger.get_point())