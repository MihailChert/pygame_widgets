import traceback

import pygame
from ..Application import AbstractController
from ..Application.builder import Builder
from .simplefigure import SimpleFigure


class DrawingController(AbstractController):

	def __init__(self, name, app, scenes, current_scene, background):
		super().__init__(name, app)
		self._scenes = scenes
		self._update_zone = None
		self._event_id = self.create_event_id()
		self._current_scene = current_scene
		self._simple_figure = None
		self.background = background

	@classmethod
	def get_settings_loader(cls, source):
		app = source.meta['application']
		app.update_option('current_scene', source.check_meta('main_scene', True))
		controller = cls(
			source.get_name(),
			app,
			source.check_meta('scenes', True),
			source.check_meta('main_scene', True),
			source.check_meta('background_color', default=pygame.Color('black'))
		)
		app.update_controller(source.get_name(), controller)
		return controller

	def init(self, app):
		self._app = app
		self.logger.info('init drawing controller')

	def after_init(self):
		for scene_name, scene_ref in self._scenes.items():
			builder = Builder.build_from(scene_ref)
			self._scenes[scene_name] = builder.build_sources(self)
		self.update_current_scene(self._current_scene)
		self._simple_figure = SimpleFigure(self._app.get_screen())

	def has_event_type(self, event_type):
		return event_type == self._event_id or event_type == self._name

	def get_node_loader(self, source):
		source.meta['controller'] = self
		cls = None
		source.meta['pos'] = source.meta.get('pos', (0, 0))
		if source.depended is None:
			source.meta['size'] = source.meta.get('size', self._app.get_screen().get_size())
		else:
			source.meta['size'] = source.meta.get('size', source.depended.meta.get('size', self._app.get_screen().get_size()))
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
			return self._current_scene
		return self._current_scene.find(needle_object)

	def destroy(self, event):
		self.logger.info('destroy controller')
		for scene in self._scenes.values():
			scene.destroy()

	def calc_update_zone(self, rect):
		if self._update_zone is None:
			self._update_zone = rect
			return
		self._update_zone = self._update_zone.union(rect)

	def update_current_scene(self, new_scene):
		self._current_scene = self._scenes[new_scene]
		self._app.update_option('current_scene', new_scene)
		self.create_event('show_scene')

	def _listen(self):
		super()._listen()
		if self._update_zone is not None:
			self._app.get_screen().fill(self.background)
			self._current_scene._draw(self)
			pygame.display.update(self._update_zone)
			self._update_zone = None
