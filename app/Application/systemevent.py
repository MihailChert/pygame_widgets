from enum import Enum
import pygame


class SystemEvent(Enum):

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
	window_icc_prof_changed = pygame.WINDOWICCPROFCHANGED  # Window ICC profile changed(SDL backend >= 2.0.18)
	window_display_change = pygame.WINDOWDISPLAYCHANGED

	@classmethod
	def values(cls):
		ret = []
		for event in cls:
			ret.append(event.value)
		return ret
