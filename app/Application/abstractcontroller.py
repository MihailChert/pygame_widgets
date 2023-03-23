from abc import abstractmethod, ABC
import pygame


class AbstractController(ABC):

	@abstractmethod
	def __init__(self, factory):
		self._event_id = self.create_event_id()
		self.event = None
		self._listeners_list = {}
		self.factory = factory

	@staticmethod
	def create_event_id():
		return pygame.event.custom_type()

	@abstractmethod
	def create_event(self, event_attrs):
		pass

	def crate_default_event(self):
		self.event = pygame.event.Event(self._event_id, method='empty_method', attrs={})

	def empty_method(self, attrs):
		pass

	@abstractmethod
	def find_object(self, needle_object):
		pass

	@abstractmethod
	def destroy(self):
		pass

	def add_listener_to(self, listened_method, handler):
		if listened_method == 'empty_method':
			raise ValueError('\'empty_method\' can\'t have any listeners')
		self._listeners_list.get(listened_method, default=[]).append(handler)

	def get_event_id(self):
		return self._event_id

	def _listen(self):
		for event in pygame.event.get(self.get_event_id()):
			try:
				getattr(self, event.method)(event.attrs_dict)
			except AttributeError:
				raise AttributeError(f'Override controller for event method {event.method} and add change in factory')
