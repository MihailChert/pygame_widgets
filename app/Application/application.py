import importlib
import importlib.util
import os
import logging
import logging.config
import pygame
from .abccontroller import AbstractController
from .source import SourceType
import pdb
'''
All action before create window and start controllers listeners
Import controllers and factories from config
'''


class Application:

	__slots__ = ['_controllers', '_single_existing', '_fps', '_clock']
	def __init__(self, controllers, logger_config):
		self._controllers = controllers
		self._single_existing = {}
		self.set_logger_config(logger_config)
		self._fps = 0
		self._clock = pygame.time.Clock()

	@classmethod
	def create_from_builder(cls, builder):
		application = cls({}, {})
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
	def _update_config(global_config, custom_config):
		for conf_fact_name, fact_conf in custom_config.items():
			if conf_fact_name not in global_config.keys():
				global_config[conf_fact_name] = fact_conf
		return global_config

	@staticmethod
	def default_logger() -> dict:
		return {
			"version": 1,
			"handlers": {
				"main_handler": {
					"class": "logging.FileHandler",
					"formatter": "standard_format",
					"filename": "app_config.log"
				}
			},
			"loggers": {
				"application": {
					"handlers": ["main_handler"],
					"level": "DEBUG",
				}
			},
			"formatters": {
				"standard_format": {
					"format": "%(levelname)-8s\t%(asctime)s\t%(name)s %(filename)s LINE %(lineno)d\t%(message)s",
					'datefmt': '%H:%M:%S'
				}
			}
		}

	def set_fps(self, new_fps):
		self._fps = new_fps

	def get_fps(self):
		return self._clock.get_fps()

	def get_clock(self):
		return self._clock

	def get_screen(self):
		try:
			return self._single_existing['screen']
		except KeyError:
			raise ValueError('Unexpected surface. Init controller before get surface.')

	def set_logger_config(self, config):
		if isinstance(config, str) and os.path.isfile(config):
			logging.config.fileConfig(config, self.default_logger())
		else:
			logging.config.dictConfig(self._update_config(self.default_logger(), config))
		self.update_option('logger', logging.getLogger('application'))

	def get_controller(self, name):
		return self._controllers[name]

	def update_controller(self, controller_name, controller):
		if not isinstance(controller, AbstractController):
			raise TypeError('Incorrect controller type. Controller must be the heir AbstractController')
		self._controllers[controller_name] = controller
		controller.init(self)

	def get_current_scene(self):
		try:
			return self._single_existing['current_scene']
		except KeyError:
			raise ValueError('Init controller before get current scene.')

	def is_option_exist(self, name):
		return self._single_existing.get(name, None) is not None

	def get_option(self, name):
		return self._single_existing[name]

	def update_option(self, name, new_val):
		self._single_existing[name] = new_val

	def update_options(self, options):
		self._single_existing.update(options)

	def get_logger(self, name=None):
		if name is None:
			return self._single_existing['logger']
		return self._single_existing['logger'].getChild(name)

	def find_loader(self, source):
		if source.get_type() == SourceType.code:
			return getattr(self, source.get_loader_method())
		elif source.get_type() == SourceType.settings:
			source.meta['application'] = self
			for c_class in source.get_dependencies():
				if c_class.get_type() == SourceType.code:
					return getattr(c_class.get_content(), source.get_loader_method())
		else:
			for controller in self._controllers.values():
				try:
					return getattr(controller, source.get_loader_method())
				except AttributeError:
					self.get_logger().warning(f'Cant find {source.get_loader_method()} in {controller.get_name()} factory')
					continue

		self.get_logger().error(
			f'Cant find loader with type {source.get_type()}. Please check method with name {source.get_loader_method()}'
			)
		raise TypeError(f'Cant find loader with type {source.get_type()}. Please check method with name {source.get_loader_method()}')

	def find_controller_by_event_type(self, event_type):
		for controller in self._controllers.values():
			if controller.has_event_type(event_type):
				return controller

	def destroy(self, event):
		for controller in self._controllers.values():
			controller.destroy(event)

	def run(self):
		for controller in self._controllers.values():
			controller.init(self)
		self._controllers['main'].after_init()
		for controller in self._controllers.values():
			controller.after_init()

		while True:
			self._clock.tick(self._fps)
			for controller in self._controllers.values():
				controller._listen()
