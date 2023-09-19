import pygame
import sys
from .abstractcontroller import AbstractController
from .systemevent import SystemEvent, MotionEvent


class AppController(AbstractController):

	def __init__(self, name, app):
		super().__init__(name, app)
		self._aliases_names = {}
		self._aliases_keys = {}
		self.add_listener(pygame.QUIT, self.destroy)
		self._app.get_logger(name).info('create controller')

	@classmethod
	def get_settings_loader(cls, source):
		config = {
			'caption': source.check_meta('caption', default='Game'),
			'display_mod': source.check_meta('display_mod', True),
			'flags': source.check_meta('flags', default=0),
			'fps': source.check_meta('fps', default=60)
		}
		app = source.meta['application']
		app.update_options(config)
		app.set_logger_config(source.check_meta('logger'))
		controller = super(cls, AppController).get_settings_loader(source)
		for alias, keys in source.check_meta('key_aliases', default={}).items():
			controller.add_alias_keys(alias, keys)
		return controller

	def init(self, app):
		if pygame.get_init():
			return
		self.logger.info('start init pygame')
		self._app = app

	def after_init(self):
		if pygame.get_init():
			return
		log = self.logger.getChild('after_init')
		pygame.init()
		log.info('finish init pygame')
		screen = pygame.display.set_mode(self._app.get_option('display_mod'), self._app.get_option('flags'))
		self._app.update_option('screen', screen)
		try:
			self.set_caption()
		except KeyError:
			log.debug('Set default pygame caption.')

	def create_event(self, event_type, **event_attrs):
		event_type = self.get_event_id(event_type)
		if event_type is not None:
			self.set_event(event_type)
		if type(event_attrs) is dict:
			event = pygame.event.Event(self._selected_event.value, **event_attrs)
		self.logger.info(f'create event {self._selected_event}')
		pygame.event.post(event)

	def add_alias_keys(self, alias, keys):
		for key in keys:
			if isinstance(key, str):
				key = pygame.key.key_code(key)
			elif isinstance(key, int):
				pass
			else:
				raise TypeError(f'Key mast be int or str not {type(key)}')
			if alias in self._aliases_names.keys():
				self._aliases_keys[key] = self._aliases_names[alias]
			else:
				handlers = []
				self._aliases_names[alias] = handlers
				self._aliases_keys[key] = handlers
		self.logger.info(self._aliases_keys)
		self.logger.info(self._aliases_names)

	def get_event_id(self, event_id_name):
		if isinstance(event_id_name, int):
			try:
				return SystemEvent(event_id_name)
			except ValueError:
				return MotionEvent(event_id_name)
		elif isinstance(event_id_name, str):
			try:
				return SystemEvent[event_id_name]
			except KeyError:
				return MotionEvent[event_id_name]

	def has_event_type(self, event_type):
		try:
			return self.get_event_id(event_type) and True
		except (ValueError, KeyError):
			return False

	def set_caption(self, new_caption=None):
		if new_caption is None:
			pygame.display.set_caption(self._app.get_option('caption'))
			return
		pygame.display.set_caption(new_caption)

	def add_listener(self, listener_method, handler, order=None):
		if listener_method == 'update':
			if order is None:
				self._listeners_update.append(handler)
			else:
				self._listeners_update.insert(order, handler)
			return
		if listener_method in self._aliases_names.keys():
			if order is None:
				self._aliases_names[listener_method].append(handler)
			else:
				self._aliases_names[listener_method].insert(order, handler)
			return
		listener_method = self.get_event_id(listener_method)
		try:
			if order is None:
				self._listeners_list[listener_method.value].append(handler)
			else:
				self._listeners_list[listener_method.value].insert(order, handler)
		except KeyError:
			self._listeners_list[listener_method.value] = [handler]
		except AttributeError:
			self.logger.error('Invalid type of event name')
			raise TypeError('Unsupported name type of event. Support string(event type by name) or int (event type).')

	def add_listener_to(self, controller_name, listener_method, handler, order=None):
		if controller_name == self.get_name():
			self.add_listener(listener_method, handler, order)
			return
		controller = self._app.get_controller(controller_name)
		controller.add_listener(listener_method, handler, order)

	def find_loader(self, source):
		try:
			return getattr(self, source.get_loader_method())
		except AttributeError:
			pass
		try:
			return self._app().find_loader(source)
		except TypeError:
			pass
		return self._app.find_loader()

	def destroy(self, event):
		if self._app.is_option_exist('game_destroy'):
			return
		self._app.update_option('game_destroy', True)
		self._app.destroy(event)
		pygame.quit()
		sys.exit()

	def _listen(self):
		for event in pygame.event.get(SystemEvent.values()):
			listeners = self._listeners_list.get(event.type, list())
			for listener in listeners:
				listener(event)
		for event in pygame.event.get(MotionEvent.values()):
			key = event.__dict__.get('key', event.__dict__.get('button', 0))
			for handler in self._aliases_keys.get(key, []):
				handler(event)
		for update_method in self._listeners_update:
			update_method(self)
