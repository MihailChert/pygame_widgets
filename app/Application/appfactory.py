import logging.config
import logging
import os
import pygame
from .abstractfactory import AbstractFactory
from .appcontroller import AppController
from .systemevent import SystemEvent
from .builder import Builder


class AppFactory:

	def __init__(self, name, app, factories, config):
		self._single_existing = {'controller': None}
		app.update_includes(name, self)
		self._name = name
		self.logger = logging.getLogger(name)
		self.set_logger_config(config.get('logger', self.default_logging()))
		self.factories = factories
		self.clock = pygame.time.Clock()
		self._single_existing.update(config)
		self._single_existing['application'] = app

	@classmethod
	def get_factory_loader(cls, source):
		config = {
			'caption': source.meta.get('caption', 'Game'),
			'display_mod': source.meta['display_mod'],
			'flags': source.meta.get('flags', 0),
			'logger': source.meta.get('logger', cls.default_logging())
		}
		app = source.meta['application']
		factories = {}
		for factory_name in source.meta['factories']:
			for dependence in source.get_dependencies():
				if dependence.get_name() == factory_name:
					factories[factory_name] = dependence.get_content()
					app.update_includes(factory_name, dependence.get_content())
		factory = cls(source.get_name(), source.meta['application'], factories, config)
		app.update_includes('main', factory)
		app.set_fps(source.meta.get('fps', 0))
		return factory

	@staticmethod
	def default_logging():
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
				"main": {
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

	@staticmethod
	def get_default_config():
		pass

	@staticmethod
	def set_logger_config(config):
		if isinstance(config, str) and os.path.isfile(config):
			logging.config.fileConfig(config)
		else:
			logging.config.dictConfig(config)

	@staticmethod
	def get_system_event():
		return SystemEvent

	@staticmethod
	def get_builder(content):
		return Builder.build_from(content)

	def update_factory(self, factory_name, factory):
		if isinstance(factory, AbstractFactory):
			self.factories[factory_name] = factory
			return
		raise ValueError('Factory mast implement AbstractFactory')

	def get_factory(self, factory_name):
		return self.factories[factory_name]

	def init(self):
		log = self.get_logger('init')

		if pygame.get_init():
			return
		log.info('init factories')
		for f_name, factory in self.factories.items():
			if factory is self:
				continue
			factory.init(f_name, self)
		log.info('finish init factories')
		log.info('init pygame')
		pygame.init()
		log.info('finish init pygame')
		self._single_existing['surface'] = pygame.display.set_mode(self._single_existing['display_mod'])
		try:
			self.get_controller().set_caption(self.get_single_object('caption'))
		except KeyError:
			log.debug('set default caption')
		except Exception as ex:
			log.error(ex)
		for factory in self.factories.values():
			if factory is self:
				continue
			factory.after_pygame_init()

	def get_controller(self):
		if not self.is_single_exist('controller'):
			self.update_single_object('controller', AppController(self))
		return self._single_existing['controller']

	def get_name(self):
		return self._name

	def is_single_exist(self, object_name):
		return self._single_existing.get(object_name, None) is not None

	def update_single_object(self, single_name, single_object=None):
		self._single_existing[single_name] = single_object

	def get_single_object(self, key):
		return self._single_existing[key]

	def get_logger(self, sub_name):
		return self.logger.getChild(sub_name)

	def get_event_id(self, module_name):
		try:
			return self.factories[module_name].get_controller().get_event_id()
		except KeyError:
			self.logger.critical(f'Not find module with name {module_name}')
			raise ValueError(f'Unexpected module with name: {module_name}')

	def get_clock(self):
		return self.clock

	def get_surface(self):
		if not self.is_single_exist('surface'):
			raise ValueError('Unexpected surface. Init factory before get surface.')
		return self._single_existing['surface']

	def get_app(self):
		if not self.is_single_exist('application'):
			raise ValueError('Unexpected application. Add application on config, before create factory')
		return self._single_existing['application']

	def get_all_controllers(self):
		controllers = [self.get_controller()]
		for factory in self.factories.values():
			controllers.append(factory.get_controller())
		return controllers
