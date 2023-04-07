import pygame
import sys
from .appfactory import AppFactory
from .abstractfactory import AbstractFactory
'''
All action before create window and start controllers listeners
Import controllers and factories from config
'''


class Application:

	INCLUDE_FACTORY = {}

	def __init__(self):
		self.factories_config = self.set_default_factories()
		self.config = self.set_default_config()
		self._main_factory = self.factories_config['main']('main', self, self.factories_config)

	@staticmethod
	def set_default_factories():
		return {'main': AppFactory}

	@staticmethod
	def set_default_config():
		return {'display_mod': (500, 500), 'display_flags': 0}

	def update_includes(self, factory_name, factory):
		self.factories_config[factory_name] = factory
		if 'main' == factory_name:
			self._main_factory = factory
		else:
			self._main_factory.update_factory(factory_name, factory)

	def run(self):
		self._main_factory.init()
		clock = self._main_factory.get_clock()
		while True:
			clock.tick()
			for controller in self._main_factory.get_all_controllers():
				controller._listen()
