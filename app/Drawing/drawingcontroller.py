import traceback

import pygame
from ..Application import AbstractController


class DrawingController(AbstractController):

	def __init__(self, factory):
		super().__init__(factory)
		self._root_node = None
		self._update_zone = None
		self._event_id = self.create_event_id()
		self._current_scene = None

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
		except AttributeError as er:
			self.logger.info(traceback.format_exc())
			self.logger.error(er)
			raise RuntimeError(f'Проверить ресурс и загружаемый класс, {cls.__name__}, {er}') #TODO: change to normal error

	def find_object(self, needle_object):
		if needle_object == 'root':
			return self._root_node
		return self._root_node.find(needle_object)

	def destroy(self, event):
		for scene in self.factory.scenes.values():
			scene.destroy()

	def calc_update_zone(self, rect):
		if self._update_zone is None:
			self._update_zone = rect
			return
		self._update_zone = self._update_zone.union(rect)

	def update_current_scene(self, new_scene):
		self._current_scene = new_scene
		self.create_event('show_scene')

	def _listen(self):
		super()._listen()
		if self._update_zone is not None:
			self.factory.get_surface().fill(self.factory.background_color)
			self._current_scene._draw(self.factory, self)
			pygame.display.update(self._update_zone)
			self._update_zone = None
