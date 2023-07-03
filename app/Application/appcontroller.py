from .abstractcontroller import AbstractController
import pygame
import sys


class AppController(AbstractController):

	def __init__(self, factory):
		super().__init__(factory)
		self._event_ids = factory.get_system_event()
		self._selected_event = None
		self.add_listener_to(pygame.QUIT, self.destroy)

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
		if isinstance(listener_method, int):
			listener_method = self._event_ids(listener_method)
		elif isinstance(listener_method, str):
			listener_method = self._event_ids[listener_method]
		try:
			self._listeners_list[listener_method.value].append(handler)
		except KeyError:
			self._listeners_list[listener_method.value] = [handler]
		except AttributeError:
			self.logger.error('Invalid type of event name')
			raise TypeError('Unsupported name type of event. Support string(event type by name) or int (event type).')

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

	def destroy(self, event):
		for controller in self.factory.get_all_controllers():
			if controller is not self:
				controller.destroy(event)
		pygame.quit()
		sys.exit()

	def _listen(self):
		for event in pygame.event.get(self._event_ids.values()):
			listeners = self._listeners_list.get(event.type, list())
			for listener in listeners:
				listener(event)
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
