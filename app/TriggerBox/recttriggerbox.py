import pygame
from .abctriggerbox import AbstractTriggerBox
import pdb


class RectTriggerBox(AbstractTriggerBox):

	def __init__(self, name, scene, parent, controller, pos, size):
		self._rect = pygame.Rect(pos, size)
		super().__init__(name, scene, parent, controller)

	@classmethod
	def create_from_source(cls, source):
		controller = source.meta['controller']
		try:
			scene = source.get_dependencies(0).get_content().get_scene()
		except (AttributeError, TypeError):
			scene = source.get_root().get_name()
		node = cls(
			source.get_name(),
			scene,
			None,
			controller,
			source.check_meta('pos', True),
			source.check_meta('size', True)
		)
		if source.check_meta('is_button', default=True):
			controller.add_button_boxes(node)
		else:
			controller.add_trigger_boxes(node)
		node._set_listeners_from_source(source)
		return node


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

	def excecute(self, event):
		print('test', event)

	def destroy(self):
		del self