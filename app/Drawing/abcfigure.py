import pygame
import numpy
from abc import ABC, abstractmethod


class AbstractFigure(ABC):

	@abstractmethod
	def __init__(self, name, parent, controller, scene, color, width, antialias):
		self._name = name
		self._parent = parent
		self._controller = controller
		self._scene = scene
		self.color = pygame.Color(color)
		self.width = width
		self.antialias = antialias

	def get_name(self):
		return self._name

	def get_parent(self):
		return self._parent

	def get_controller(self):
		return self._controller

	def get_scene(self):
		return self._scene

	def on_scene(self, scene):
		return self._scene == scene

	def get_global_rect(self):
		return self._parent.convert_rect_to_global(self.get_rect())

	def connect_events_from_source(self, source):
		for controller_name, listeners in source.check_meta('listeners', default={}).items():
			for listener_method, listener_handler in listeners.items():
				self.handler_by_controller(controller_name, listener_method, getattr(self, listener_handler), source)

	def handler_by_controller(self, controller_name, listener_method, listener_handler, source):
		self._controller.add_listener_to(controller_name, listener_method, listener_handler)

	@classmethod
	def create_from_source(cls, source):
		pass

	@abstractmethod
	def get_rect(self, points):
		pass

	@abstractmethod
	def move(self, delta_x=0, delta_y=0):
		pass

	@abstractmethod
	def resize(self, scale_x=0, scale_y=0):
		pass

	@abstractmethod
	def update_pos(self, x=None, y=None):
		pass

	@abstractmethod
	def rotate(self, align, radians=False):
		pass
	
	@staticmethod
	def deg2rad(degrees):
		return numpy.deg2rad(degrees)

	@staticmethod
	def rad2deg(radians):
		return numpy.rad2deg(radians)

	@abstractmethod
	def _draw(self):
		pass

	def destroy(self):
		pass