from enum import Enum
from .abstractcontroller import AbstractController
import pygame
import sys


class AppController(AbstractController):

	def __init__(self):
		self._event_ids = SystemEvents
		self._selected_event = None

	def create_event(self, event_attrs):
		if self._selected_event is None:
			raise ValueError('Set event type before create')
		if type(event_attrs) is dict:
			event = pygame.event.Event(self._selected_event.value, **event_attrs)
		if type(event_attrs) is list:
			event = pygame.event.Event(self._selected_event.value, *event_attrs)
		self._selected_event = None
		return event

	def get_event_id(self):
		return self._selected_event

	def destroy(self):
		pass

	def _listen(self):
		for event in pygame.event.get(self._event_ids.values()):
			method = self._event_ids(event.type)
			try:
				getattr(self, method.name)(event)
			except AttributeError as er:
				# TODO: log error
				print(er)
				self.empty_method(event)

	def quit(self, event):
		pygame.quit()
		sys.exit()

	def set_event(self, event_name_or_id):
		if event_name_or_id in self._event_ids:
			self._selected_event = event_name_or_id

	def find_object(self, needle_object):
		pass


class SystemEvents(Enum):

	quit = pygame.QUIT
	window_shown = pygame.WINDOWSHOWN
	window_hidden = pygame.WINDOWHIDDEN
	window_exposed = pygame.WINDOWEXPOSED
	window_moved = pygame.WINDOWMOVED
	window_resized = pygame.WINDOWRESIZED
	window_resize_changed = pygame.WINDOWSIZECHANGED
	window_minimized = pygame.WINDOWMINIMIZED
	window_maximized = pygame.WINDOWMAXIMIZED
	window_restored = pygame.WINDOWRESTORED
	window_enter = pygame.WINDOWENTER
	window_leave = pygame.WINDOWLEAVE
	window_focus_gained = pygame.WINDOWFOCUSGAINED
	window_focus_lost = pygame.WINDOWFOCUSLOST
	window_close = pygame.WINDOWCLOSE
	window_take_focus = pygame.WINDOWTAKEFOCUS  # Window was offered focus(SDL backend >= 2.0.5)
	window_hit_test = pygame.WINDOWHITTEST  # Window has a special hit test(SDL backend >= 2.0.5)
	# window_icc_prof_changed = pygame.WINDOWICCPROFCHANGED  # Window ICC profile changed(SDL backend >= 2.0.18)
	# window_display_change = pygame.WINDOWDISPLAYCHANGED

	@classmethod
	def values(cls):
		ret = []
		for event in cls:
			ret.append(event.value)
		return ret
