import pygame
from .abctriggerbox import AbstractTriggerBox


class RectTriggerBox(AbstractTriggerBox):

	@classmethod
	def create_from_source(cls, source):
		controller = source.meta['controller']
		try:
			scene = source.get_dependencies(0).get_content().get_scene()
		except (AttributeError, TypeError):
			scene = source.get_root().get_name()
		node = cls(
			source.get_name(),
			source.check_meta('pos', True),
			source.check_meta('size', True),
			scene,
			None,
			controller
		)
		if source.check_meta('is_button', default=True):
			controller.add_button_boxes(node)
		else:
			controller.add_trigger_boxes(node)
		node._set_listeners_from_source(source)
		return node

	def destroy(self):
		pass

	def _collide_rule_object(self, trigger):
		return self.get_global_rect().colliderect(trigger.get_global_rect())

	def _collide_rule_point(self, point):
		return self.get_global_rect().collidepoint(point)

	def _contain_rule_object(self, trigger):
		return self.get_global_rect().contains(trigger.get_global_point())

	def excecute(self, event):
		if self._collide_rule_point(event.pos):
			print('test', event)