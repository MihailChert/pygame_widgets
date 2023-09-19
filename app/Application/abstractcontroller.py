from abc import abstractmethod, ABC
import pygame


class AbstractController(ABC):

	@abstractmethod
	def __init__(self, name, app):
		self._name = name
		self._app = app
		self.logger = app.get_logger().getChild(name)
		self.logger.info('init controller')
		self._listeners_list = {}
		self._listeners_update = []

	def __str__(self):
		return f'<Controller {self._name}>'

	@classmethod
	@abstractmethod
	def get_settings_loader(cls, source):
		app = source.meta['application']
		controller = cls(source.get_name(), app)
		app.update_controller(source.get_name(), controller)
		return controller
	@abstractmethod
	def init(self, app):
		self._app = app

	@abstractmethod
	def after_init(self):
		pass

	@abstractmethod
	def has_event_type(self, event_type):
		pass

	@staticmethod
	def create_event_id():
		return pygame.event.custom_type()

	@staticmethod
	def get_default_config():
		return {}

	def get_name(self):
		return self._name

	def get_app(self):
		return self._app


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

	def find_loader(self, source):
		try:
			return getattr(self, source.get_loader_method())
		except AttributeError:
			return self._app.find_loader(source)

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

	def add_listener_to(self, controller_name, listener_method, handler, order=None):
		if controller_name == self._name:
			self.add_listener(listener_method, handler, order)
			return
		controller = self._app.get_controller(controller_name)
		controller.add_listener(listener_method, handler, order)

	def get_event_id(self):
		return self._event_id

	def _listen(self):
		for event in pygame.event.get(self.get_event_id()):
			listeners = self._listeners_list.get(event.method, [])
			for handler in listeners:
				handler(event)
		for update_method in self._listeners_update:
			update_method(self)
