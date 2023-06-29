from .abstractcontroller import AbstractController
import pygame
import sys


class AppController(AbstractController):

	def __init__(self, factory):
		self._event_ids = factory.get_system_event()
		self._selected_event = None
		self.factory = factory
		self.logger = factory.get_logger('Controller')
		self._listeners_list = {}
		self._listeners_update = []
		self.event = None

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

	def create_event_id(self):
		return self._event_ids

	def get_event_id(self):
		return self._selected_event

	@staticmethod
	def set_caption(new_caption):
		pygame.display.set_caption(new_caption)

	def add_listener_to(self, listener_method, handler):
		try:
			listener_method = self._event_ids['listener_method']
		except KeyError:
			raise KeyError('')
		try:
			self._listeners_list[listener_method.value].append(handler)
		except KeyError:
			self._listeners_list[listener_method.value] = [handler]

	def find_loader(self, source):
		try:
			return getattr(self.factory, source.get_loader_method())
		except AttributeError:
			pass
		for factory in self.factroy.factories.values():
			try:
				return getattr(factory, source.get_loader_method())
			except AttributeError:
				self.logger.warning(f'Cant find {source.get_logger_method()} in {factory.get_name()} factory')
				continue
		self.logger.error(f'Cant find loader with type {source.get_type()}. Please check method with name {source.get_loader_method()}')
		raise TypeError(f'Cant find loader with type {source.get_type()}. Please check method with name {source.get_loader_method()}')

	def destroy(self):
		pass

	def _listen(self):
		for event in pygame.event.get(self._event_ids.values()):
			listeners = self._listeners_list.get(event.type, list())
			for listener in listeners:
				listener(event)
		for update_method in self._listeners_update:
			update_method(self)

	@staticmethod
	def quit(event):
		pygame.quit()
		sys.exit()

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
