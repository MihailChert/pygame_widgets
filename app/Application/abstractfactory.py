from abc import ABC, abstractmethod


class AbstractFactory(ABC):

	@abstractmethod
	def __init__(self, name, main_factory, factory_config):
		self._single_existing = {'controller': None, 'logger': None}
		self._name = name
		self._main_factory = main_factory
		self.logger = None

	@abstractmethod
	def init(self, name, main_factory):
		self._main_factory = main_factory
		self.logger = main_factory.get_logger(name)

	@classmethod
	@abstractmethod
	def get_settings_loader(cls, source):
		pass

	@abstractmethod
	def after_pygame_init(self):
		pass

	@staticmethod
	@abstractmethod
	def get_default_config():
		pass

	def get_name(self):
		return self._name

	def get_main_factory(self):
		return self._main_factory

	def is_single_exist(self, object_name):
		return self._single_existing.get(object_name, None) is not None

	def update_single_object(self, single_name, single_object=None):
		self._single_existing[single_name] = single_object

	def get_logger(self, sub_name):
		return self.logger.getChild(sub_name)

	@abstractmethod
	def get_controller(self):
		pass
