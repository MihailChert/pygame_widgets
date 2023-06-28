import pygame
from ..Application import AbstractController


class DrawingController(AbstractController):

	def __init__(self, factory):
		super().__init__(factory)
		self._root_node = None
		self._update_zone = pygame.Rect(0, 0, 0, 0)

	def create_event(self, method, event_attrs):
		event = pygame.event.Event(self._event_id)
		event.__dict__['method'] = method
		event.__dict__.update(event_attrs)
		return event

	def find_object(self, needle_object):
		if needle_object == 'root':
			return self._root_node
		return self._root_node.find(needle_object)

	def destroy(self):
		self._root_node.destroy()

	def get_root_node(self):
		if self._root_node is None:
			self._root_node = self.factory.get_node('root', (0, 0), self.factory.get_surface().get_size(), None)
			self._listeners_update.append(self._root_node.update)
		return self._root_node

	def calc_update_zone(self, rect):
		self._update_zone = self._update_zone.union(rect)

	def _listen(self):
		super()._listen()
		self.get_root_node()._draw_node(self.factory, self)
		pygame.display.update(self._update_zone)
		self._update_zone = pygame.Rect(0, 0, 0, 0)
