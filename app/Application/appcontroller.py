import pygame
import sys
from .abccontroller import AbstractController
from .systemevent import SystemEvent


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
			'caption': source.check_meta('caption', default='pygame game'),
			'fps': source.check_meta('fps', default=60)
		}
		app = source.meta['application']
		app.update_options(config)
		app.set_logger_config(source.check_meta('logger'))
		controller = super(cls, AppController).get_settings_loader(source)
		return controller

	def before_init(self, app):
		if pygame.get_init():
			return
		self.logger.info('start before init pygame')
		super().before_init(app)

	def init(self):
		if pygame.get_init():
			return
		log = self.logger.getChild('init')
		pygame.init()
		log.info('finish init pygame')
		try:
			self.set_caption()
		except KeyError:
			log.debug('Set default pygame caption.')

	def create_event(self, event_type, **event_attrs): # revrite used attributes in SourceType
		event_type = self.get_event_id(event_type)
		if event_type is not None:
			self.set_event(event_type)
		if type(event_attrs) is dict:
			event = pygame.event.Event(self._selected_event.value, **event_attrs)
		self.logger.info(f'create event {self._selected_event}')
		pygame.event.post(event)

	def get_event_id(self, event_id_name):
		if isinstance(event_id_name, int):
			try:
				return SystemEvent(event_id_name)
			except ValueError:
				self.logger.error('Ivalid event type given: ' + event_id_name)
		elif isinstance(event_id_name, str):
			try:
				return SystemEvent[event_id_name]
			except KeyError:
				self.logger.error('Invalid event name given: ' + event_id_name)
				
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

	def add_listener(self, listened_method, handler, order=None):
		self.logger.debug(f'Add listener method \'{listened_method}\' to controller {self.get_name()}, with order {order}')
		if listened_method == 'update':
			if order is None:
				self._listeners_update.append(handler)
			else:
				self._listeners_update.insert(order, handler)
			return
		if listened_method in self._aliases_names.keys():
			if order is None:
				self._aliases_names[listened_method].append(handler)
			else:
				self._aliases_names[listened_method].insert(order, handler)
			return
		try:
			listened_method = self.get_event_id(listened_method)
			if order is None:
				self._listeners_list[listened_method.value].append(handler)
			else:
				self._listeners_list[listened_method.value].insert(order, handler)
		except KeyError:
			self._listeners_list[listened_method.value] = [handler]
		except AttributeError:
			self.logger.error(f'Invalid type of event name {listened_method}.')
			raise TypeError(f'Unsupported name type of event. Support string(event type by name) or int (event type): {listener_method}.')

	def add_listener_to(self, controller_name, listened_method, handler, order=None):
		if controller_name == self.get_name():
			self.add_listener(listened_method, handler, order)
			return
		controller = self._app.get_controller(controlled_name)
		controller.add_listener(listened_method, handler, order)

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
		if self._app.is_option_exist('game_destroied'):
			return
		self._app.update_option('game_destroied', True)
		self._app.destroy(event)
		self.logger.info('destroy controller ' + self.get_name())
		pygame.quit()
		sys.exit()

	def _listen(self):
		for event in pygame.event.get(SystemEvent.values()):
			listeners = self._listeners_list.get(event.type, list())
			for listener in listeners:
				listener(event)
		for update_method in self._listeners_update:
			if self._app.is_option_exist('current_scene')\
				and update_handler.__self__.on_scene(
					self._app.get_option('current_scene')
				):
				update_method(self)
