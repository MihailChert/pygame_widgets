from abc import abstractmethod
import pygame
from ..Application import AbstractPhysicalNode


class AbstractTriggerBox(AbstractPhysicalNode):

	def _set_listeners_from_source(self, source):
		for controller_name, listeners in source.check_meta('listeners', default={}).items():
			for listener_method, listener_handler in listeners.items():
				self.handle_by_controller(controller_name, listener_method, getattr(self, listener_handler), source)

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