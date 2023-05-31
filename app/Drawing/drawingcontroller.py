import pygame
from ..Application import AbstractController


class DrawingController(AbstractController):

	def __init__(self, factory):
		super().__init__(factory)

	def create_event(self, event_attrs):
		pass

	def find_object(self, needle_object):
		pass

	def destroy(self):
		pass

	def calc_update_zone(self):
		pass

	def _listen(self):
		self.factory.fill_background()
		super()._listen()
		update_rect = self.calc_update_zone()
		pygame.display.update(update_rect)
