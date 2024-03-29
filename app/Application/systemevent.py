from enum import Enum
import pygame


class EnginEnum(Enum):

	@classmethod
	def values(cls):
		ret = []
		for event in cls:
			ret.append(event.value)
		return ret

class SystemEvent(EnginEnum):

	quit = pygame.QUIT
	resize = pygame.VIDEORESIZE
	expose = pygame.VIDEOEXPOSE
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


class MotionEvent(EnginEnum):

	key_down = pygame.KEYDOWN
	key_up = pygame.KEYUP
	mouse_move = pygame.MOUSEMOTION
	mouse_key_down = pygame.MOUSEBUTTONDOWN
	mouse_key_up = pygame.MOUSEBUTTONUP
	joy_axis_move = pygame.JOYAXISMOTION
	joy_boll_move = pygame.JOYBALLMOTION
	joy_hat_move = pygame.JOYHATMOTION
	joy_key_down = pygame.JOYBUTTONDOWN
	joy_key_up = pygame.JOYBUTTONUP
