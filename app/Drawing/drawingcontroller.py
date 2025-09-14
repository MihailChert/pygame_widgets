import traceback
import pygame
import warnings
from ..Application import AbstractController
from ..Application.builder import Builder


class DrawingController(AbstractController):

	def __init__(self, name, app, scenes, current_scene, window_size, flags, background):
		super().__init__(name, app)
		self._screen = None
		self._size = window_size
		self._scenes = scenes
		self._flags = flags
		self._update_zone = None
		self._event_id = self.create_event_id()
		self._current_scene = current_scene
		self._simple_figure = None
		self.background = background

	@classmethod
	def get_settings_loader(cls, source):
		app = source.meta['application']
		app.update_option('current_scene', source.check_meta('main_scene', True))
		flags = 0
		for flag in source.check_meta('window_flags', default=list()):
			try:
				flags |= getattr(pygame, flag)
			except AttributeError:
				warnings.warn(f'Unexpected flag: {flag}.')
		controller = cls(
			source.get_name(),
			app,
			source.check_meta('scenes', True),
			source.check_meta('main_scene', True),
			source.check_meta('window_size', True),
			flags,
			source.check_meta('background_color', default=pygame.Color('black'))
		)
		app.update_controller(source.get_name(), controller)
		return controller

	def before_init(self, app):
		pygame.display.init()
		super().before_init(app)

	def init(self):
		self._size = self.parse_size(self._size)
		self._create_dispaly()
		self._app.update_option('screen', self._screen)
		for scene_name, scene_ref in self._scenes.items():
			builder = Builder.build_from(scene_ref)
			self.logger.info('create scene ' + scene_name)
			self._scenes[scene_name] = builder.build_sources(self)
			if self._scenes[scene_name].get_name() != scene_name:
				raise RuntimeError('Invalid root node name. Root node name must be equal scene name.')
		self.update_current_scene(self._current_scene)

	@staticmethod
	def get_list_sizes():
		return pygame.display.list_modes()

	@staticmethod
	def get_window_size():
		return pygame.display.get_window_size()

	@staticmethod
	def parse_size(size):
		if isinstance(size, str):
			index = size.split('_')
			try:
				index = int(index[1])
			except ValueError:
				raise IndexError(f'Cant parse index for list sizes: {index[1]}')
			return pygame.display.list_modes()[index]
		if isinstance(size, (list, set)):
			return size

	def fullscreen(self, fullscreen_flag=None):
		if fullscreen_flag is None:
			pygame.display.toggle_fullscreen()
			return
		if fullscreen_flag and not self._flags & pygame.FULLSCREEN:
			self._flags |= pygame.FULLSCREEN
			pygame.display.toggle_fullscreen()
			return
		if not fullscreen_flag and self._flags & pygame.FULLSCREEN:
			self._flags -= pygame.FULLSCREEN
			pygame.display.toggle_fullscreen()

	def set_size(self, new_size):
		self._size = new_size
		self._create_dispaly()

	def _create_dispaly(self):
		pygame.display.quit()
		pygame.display.init()
		self._screen = pygame.display.set_mode(self._size, self._flags)
		self._app.update_option('screen', self._screen)

	def get_node_loader(self, source):
		source.meta['controller'] = self
		cls = None
		source.meta['pos'] = source.meta.get('pos', (0, 0))
		if not len(source.meta['pos']):
			source.meta['pos'] = (0, 0)
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

	def get_simple_figure(self):
		return self._simple_figure

	def find_object(self, needle_object):
		if needle_object == 'root':
			return self._current_scene
		return self._current_scene.find(needle_object)

	def destroy(self, event):
		self.logger.info('destroy controller ' + self.get_name())
		for scene in self._scenes.values():
			scene.destroy()

	def calc_update_zone(self, rect):
		self._update_zone = True
		# if self._update_zone is None:
		# 	self._update_zone = rect
		# 	return
		# self._update_zone = self._update_zone.union(rect)

	def update_current_scene(self, new_scene):
		self._current_scene = self._scenes[new_scene]
		self._app.update_option('current_scene', new_scene)
		self.create_event('show_scene')

	def _listen(self):
		super()._listen()
		if self._update_zone is not None:
			self._app.get_screen().fill(self.background)
			self._current_scene._draw()
			pygame.display.update()
			self._update_zone = None
