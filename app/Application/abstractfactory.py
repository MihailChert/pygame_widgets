from abc import ABC, abstractmethod


class AbstractFactory(ABC):

	@abstractmethod
	def __init__(self, name, app):
		self._single_existing = {'controller': None, 'logger': None}
		app.update_includes(name, self)
		self._name = name
		self._app = app

	@abstractmethod
	def init(self):
		pass

	def get_name(self):
		return self._name

	def get_app(self):
		return self._app

	def is_single_exist(self, object_name):
		return self._single_existing.get(object_name, None) is not None

	def update_single_object(self, single_name, single_object=None):
		self._single_existing[single_name] = single_object

	def get_logger(self, sub_name=''):
		return self.logger.getLogger(sub_name)

	@abstractmethod
	def get_controller(self):
		pass
