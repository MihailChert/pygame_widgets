import pygame
from ..Application import AbstractController


class DrawingController(AbstractController):

	def __init__(self, factory):
		super().__init__(factory)
		self._root_node = None
		self._update_zone = pygame.Rect(0, 0, 0, 0)
		self._event_id = self.create_event_id()

	def get_node_loader(self, source):
		source.meta['controller'] = self
		cls = None
		source.meta['pos'] = source.meta.get('pos', (0, 0))
		if source.depended is None:
			source.meta['size'] = source.meta.get('size', self.factory.get_surface().get_size())
		else:
			source.meta['size'] = source.meta.get('size', source.depended.meta.get('size', self.factory.get_surface().get_size()))
		for dependence in source.get_dependencies():
			if dependence.get_name() == source.get_source():
				cls = dependence.get_content()
				break
		try:
			return cls.create_from_source(source)
		except AttributeError:
			raise RuntimeError('Проверить ресурс и загружаемый класс') #TODO: change to normal error

	def create_event(self, method, event_attrs):
		event = pygame.event.Event(self._event_id)
		event.__dict__['method'] = method
		event.__dict__.update(event_attrs)
		return event

	def find_object(self, needle_object):
		if needle_object == 'root':
			return self._root_node
		return self._root_node.find(needle_object)

	def destroy(self, event):
		for scene in self.factory.scenes.values():
			scene.destroy()

	def get_root_node(self):
		return self.factory.scenes[self.factory.main_scene]

	def calc_update_zone(self, rect):
		self._update_zone = self._update_zone.union(rect)

	def _listen(self):
		super()._listen()
		self.factory.get_surface().fill(self.factory.background_color)
		self.get_root_node()._draw_node(self.factory, self)
		pygame.display.update(self._update_zone)
		self._update_zone = pygame.Rect(0, 0, 0, 0)
