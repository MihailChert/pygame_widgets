from abc import abstractmethod, ABC
import pygame


class AbstractController(ABC):

	@abstractmethod
	def __init__(self, factory):
		self.logger = factory.get_logger('Controller')
		self.logger.info('init controller')
		self._listeners_list = {}
		self._listeners_update = []
		self.factory = factory
		self.event = None

	@staticmethod
	def create_event_id():
		return pygame.event.custom_type()

	@abstractmethod
	def create_event(self, method, event_attrs):
		if method not in self._listeners_list.keys():
			self.logger.warn('Event method has no listeners')
		event = pygame.event.Event(self._event_id, method=method, **event_attrs)
		self.event = event

	def crate_default_event(self):
		self.event = pygame.event.Event(self._event_id, method='empty_method', attrs={})

	def post(self):
		if isinstance(self.event, pygame.event.Event):
			pygame.event.post(self.event)
		elif self.event is not None:
			self.logger.critical('Unsupported event type.')
			raise TypeError('Unsupported type for posted event.')
		else:
			self.logger.warn('Create event before post.')

	def empty_method(self, attrs):
		self.logger.info('Call empty method')

	@abstractmethod
	def find_object(self, needle_object):
		pass

	def find_loader(self, source):
		try:
			return getattr(self, source.get_loader_method())
		except AttributeError:
			return self.factory.get_main_factory().get_controller().find_loader(source)

	@abstractmethod
	def destroy(self, event):
		pass

	def add_listener_to(self, listened_method, handler):
		if listened_method == 'empty_method':
			self.logger.error('add listener to empty method')
			raise ValueError('\'empty_method\' can\'t have any listeners')
		try:
			self._listeners_list[listened_method].append(handler)
		except KeyError:
			self._listeners_list[listened_method] = [handler]

	def get_event_id(self):
		return self._event_id

	def _listen(self):
		for event in pygame.event.get(self.get_event_id()):
			listeners = self._listeners_list.get(event.method)
			for handler in listeners:
				handler(event)
		for update_method in self._listeners_update:
			update_method(self)
