import pdb

from .abstractfactory import AbstractFactory
from .appcontroller import AppController
import logging.config
import logging
import os
import pygame


class AppFactory:

	def __init__(self, name, app, factories):
		self._single_existing = {'controller': None}
		app.update_includes(name, self)
		self._name = name
		self._app = app
		self.logger = logging.getLogger(name)
		self.set_logger_config(app.config.get('logger', self.default_logging()))
		self.factories = factories
		self.clock = pygame.time.Clock()
		self._single_existing['display_mod'] = app.config['main']['display_mod']

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

	def update_factory(self, factory_name, factory):
		if isinstance(factory, AbstractFactory):
			self.factories[factory_name] = factory
			return
		raise ValueError('Factory mast implement AbstractFactory')

	def init(self):
		log = self.get_logger('init')

		if pygame.get_init():
			return
		log.info('init factories')
		for f_name, factory in self.factories.items():
			if factory is self:
				continue
			fact_conf = self._app.config.get(f_name, dict())
			factory.init(f_name, self, fact_conf)
		log.info('finish init factories')
		log.info('init pygame')
		pygame.init()
		log.info('finish init pygame')
		self._single_existing['surface'] = pygame.display.set_mode(self._single_existing['display_mod'])
		try:
			self.get_controller().set_caption(self._app.config['caption'])
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
		controllers = []
		print(self.factories)
		for factory in self.factories.values():
			print(factory)
			controllers.append(factory.get_controller())
		return controllers
