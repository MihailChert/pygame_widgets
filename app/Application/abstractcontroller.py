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

	@staticmethod
	def create_event_id():
		return pygame.event.custom_type()

	def create_event(self, method, **event_attrs):
		if method not in self._listeners_list.keys():
			self.logger.warn('Event method has no listeners')
		if not event_attrs:
			event = pygame.event.Event(self._event_id, method=method)
		else:
			event_attrs['method'] = method
			event = pygame.event.Event(self._event_id, event_attrs)
		pygame.event.post(event)

	def crate_default_event(self):
		pygame.event.post(pygame.event.Event(self._event_id, method='empty_method', attrs={}))

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

	def add_listener(self, listened_method, handler, order=None):
		if listened_method == 'empty_method':
			self.logger.error('add listener to empty method')
			raise ValueError('\'empty_method\' can\'t have any listeners')
		if listened_method == 'update':
			if order is None:
				self._listeners_update.append(handler)
			else:
				self._listeners_update.insert(order, handler)
			return
		try:
			if order is None:
				self._listeners_list[listened_method].append(handler)
			else:
				self._listeners_list[listened_method].insert(order, handler)
		except KeyError:
			self._listeners_list[listened_method] = [handler]

	def add_listener_to(self, factory_name, listener_method, handler, order=None):
		if factory_name == self.factory.get_name():
			self.add_listener(listener_method, handler, order)
			return
		controller = self.factory.get_main_factory().get_factory(factory_name)
		controller = controller.get_controller()
		controller.add_listener(listener_method, handler, order)

	def get_event_id(self):
		return self._event_id

	def _listen(self):
		for event in pygame.event.get(self.get_event_id()):
			listeners = self._listeners_list.get(event.method)
			for handler in listeners:
				handler(event)
		for update_method in self._listeners_update:
			update_method(self)
