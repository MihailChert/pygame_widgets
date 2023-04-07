import pdb

from .abstractfactory import AbstractFactory
from .appcontroller import AppController
import logging.config
import pygame


class AppFactory(AbstractFactory):

	def __init__(self, name, app, factories):
		super().__init__(name, app)
		self.factories = factories
		self.clock = pygame.time.Clock()
		self._single_existing['display_mod'] = app.config['display_mod']

	@staticmethod
	def default_logging():
		return {}
		# return {
		# 	"version": 1,
		# 	"handlers": {
		# 		"fileHandler": {
		# 			"class": "logging.FileHandler",
		# 			"formatter": "myFormatter",
		# 			"filename": "app_config.log"
		# 		}
		# 	},
		# 	"loggers": {
		# 		"application_logger": {
		# 			"handlers": ["fileHandler"],
		# 			"level": "DEBUG",
		# 		}
		# 	},
		# 	"formatters": {
		# 		"standard_format": {
		# 			"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
		# 		}
		# 	}
		# }

	def update_factory(self, factory_name, factory):
		if isinstance(factory, AbstractFactory):
			self._single_existing[factory_name] = factory
			return
		raise ValueError('Factory mast implement AbstractFactory')

	def init(self):
		if pygame.get_init():
			return
		pygame.init()
		for factory in self.factories.values():
			factory.init()
		self._single_existing['surface'] = pygame.display.set_mode(self._single_existing['display_mod'])
		try:
			self.get_controller().set_cation(self._app.config['caption'])
		except KeyError:
			pass

	def get_controller(self):
		if not self.is_single_exist('controller'):
			self.update_single_object('controller', AppController())
		return self._single_existing['controller']

	def get_event_id(self, module_name):
		try:
			return self.factories[module_name].get_controller().get_event_id()
		except KeyError:
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
		for factory in self.factories.values():
			controllers.append(factory.get_controller())
		return controllers
