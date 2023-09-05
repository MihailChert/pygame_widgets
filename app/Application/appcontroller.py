from .abstractcontroller import AbstractController
import pygame
import sys
import pdb


class AppController(AbstractController):

	def __init__(self, factory):
		super().__init__(factory)
		self._system_ids = factory.get_system_event()
		self._motion_ids = factory.get_motion_event()
		self._selected_event = None
		self._aliases_names = {}
		self._aliases_keys = {}
		self.add_listener(pygame.QUIT, self.destroy)
		self.factory.get_logger('controller').info('create_logger')

	def create_event(self, event_type, event_attrs):
		if self._selected_event is None:
			self.logger.error('event type dont set')
			raise ValueError('Set event type before create')
		if event_type is not None:
			self.set_event(event_type)
		if type(event_attrs) is dict:
			event = pygame.event.Event(self._selected_event.value, **event_attrs)
		if type(event_attrs) is list:
			event = pygame.event.Event(self._selected_event.value, *event_attrs)
		self._selected_event = None
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
				return self._system_ids(event_id_name)
			except ValueError:
				return self._motion_ids(event_id_name)
		elif isinstance(event_id_name, str):
			try:
				return self._system_ids[event_id_name]
			except KeyError:
				return self._motion_ids[event_id_name]

	@staticmethod
	def set_caption(new_caption):
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
		if controller_name == self.factory.get_name():
			self.add_listener(listener_method, handler, order)
			return
		controller = self.factory.get_factory(controller_name).get_controller()
		controller.add_listener(listener_method, handler, order)

	def find_loader(self, source):
		try:
			return getattr(self, source.get_loader_method())
		except AttributeError:
			pass
		try:
			return self.factory.get_app().find_loader(source)
		except TypeError:
			pass
		for factory in self.factory.factories.values():
			try:
				return getattr(factory.get_controller(), source.get_loader_method())
			except AttributeError:
				self.logger.warning(f'Cant find {source.get_loader_method()} in {factory.get_name()} factory')
				continue
		self.logger.error(f'Cant find loader with type {source.get_type()}. Please check method with name {source.get_loader_method()}')
		raise TypeError(f'Cant find loader with type {source.get_type()}. Please check method with name {source.get_loader_method()}')

	def destroy(self, event):
		for controller in self.factory.get_all_controllers():
			if controller is not self:
				controller.destroy(event)
		pygame.quit()
		sys.exit()

	def _listen(self):
		for event in pygame.event.get(self._system_ids.values()):
			listeners = self._listeners_list.get(event.type, list())
			for listener in listeners:
				listener(event)
		for event in pygame.event.get(self._motion_ids.values()):
			key = event.__dict__.get('key', event.__dict__.get('button', 0))
			for handler in self._aliases_keys.get(key, []):
				handler(event)
		for update_method in self._listeners_update:
			update_method(self)

	def set_event(self, event_name_or_id):
		self.logger.info(f'try set event {event_name_or_id}')
		if isinstance(event_name_or_id, int):
			event_name_or_id = self._event_ids(event_name_or_id)
		elif isinstance(event_name_or_id, str):
			event_name_or_id = self._event_ids[event_name_or_id]
		if event_name_or_id in self._event_ids:
			self._selected_event = event_name_or_id

	def find_object(self, needle_object):
		pass
