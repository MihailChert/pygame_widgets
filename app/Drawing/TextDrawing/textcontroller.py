import pygame
from ...Application.abstractcontroller import AbstractController


class TextController(AbstractController):

	def __init__(self, factory):
		super().__init__(factory)
		self.__drawing_controller = factory.get_drawing_factory().get_controller()
		self._event_id = self.__drawing_controller.get_event_id()

	def find_object(self, needle_object):
		pass

	def destroy(self, event):
		pygame.font.quit()

	def add_listener_to(self, listened_method, handler):
		if listened_method == 'empty_method':
			self.logger.error('add listener to empty method')
			raise ValueError('\'empty_method\' can\'t have any listeners')
		self.__drawing_controller.add_listener_to('text_'+listened_method, handler)

	def _listen(self):
		pass
