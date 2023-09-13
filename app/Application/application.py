import importlib
import importlib.util
from .appfactory import AppFactory
from .source import SourceType
'''
All action before create window and start controllers listeners
Import controllers and factories from config
'''


class Application:

	INCLUDE_FACTORY = {}

	def __init__(self, factories=dict()):
		self.factories_config = factories
		self._fps = 0
		self._main_factory = self.factories_config.get('main', AppFactory)('main', self, self.factories_config, {})

	@classmethod
	def create_from_builder(cls, builder):
		application = cls()
		builder.build_sources(application)
		return application

	@staticmethod
	def get_code_loader(source):
		try:
			module = importlib.import_module(source.get_source())
		except ModuleNotFoundError:
			file_spec = importlib.util.spec_from_file_location(source.get_source().split('.')[-1], source.get_source().replace('.', '/')+'.py')
			module = importlib.util.module_from_spec(file_spec)
			file_spec.loader.exec_module(module)
		return getattr(module, source.get_name())

	@staticmethod
	def get_default_factories():
		return {'main': AppFactory}

	@staticmethod
	def _update_config(global_config, custom_config):
		for conf_fact_name in global_config.keys():
			if conf_fact_name in custom_config.keys():
				global_config[conf_fact_name].update(custom_config[conf_fact_name])
		for conf_fact_name, fact_conf in custom_config.items():
			if conf_fact_name not in global_config.keys():
				global_config[conf_fact_name] = fact_conf
		return global_config

	def set_fps(self, new_fps):
		self._fps = new_fps

	def find_loader(self, source):
		if source.get_type() == SourceType.code:
			return getattr(self, source.get_loader_method())
		elif source.get_type() == SourceType.settings:
			source.meta['application'] = self
			for factory_class in source.get_dependencies():
				if factory_class.get_type() == SourceType.code:
					return getattr(factory_class.get_content(), source.get_loader_method())
		raise TypeError(f'Cant find loader with type {source.get_type()}. Please check method with name {source.get_loader_method()}')

	def update_includes(self, factory_name, factory):
		self.factories_config[factory_name] = factory
		if 'main' == factory_name:
			self._main_factory = factory
		else:
			self._main_factory.update_factory(factory_name, factory)

	def run(self):
		self._main_factory.init()
		clock = self._main_factory.get_clock()
		controllers = self._main_factory.get_all_controllers()
		while True:
			clock.tick(self._fps)
			for controller in controllers:
				controller._listen()
