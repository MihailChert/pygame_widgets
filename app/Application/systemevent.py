from enum import Enum, EnumType, EnumMeta
import pygame
import pdb


class EnginEnumUnion(type):
	
	def __new__(metacls, clsname, clsattrs, union_enums):
		if isinstance(union_enums, EnumType):
			union_enums = [union_enums]
		elif isinstance(union_enums, list):
			for e in union_enums:
				if not isinstance(e, EnumType):
					raise ValueError('List set, not enums type: %s' % type(e))
		clsattrs['__enums__'] = union_enums
		clsattrs['__name__'] = clsname
		clsattrs['__repr__'] = Enum.__repr__
		clsattrs['__str__'] = Enum.__str__
		return super().__new__(metacls, clsname, (), clsattrs)

	def __getattr__(cls, name):
		for enum in cls.__enums__:
			try:
				return enum[name]
			except KeyError:
				continue
		raise AttributeError(name)

	def __getitem__(cls, key):
		for enum in cls.__enums__:
			try:
				return enum[key]
			except KeyError as e:
				continue
		raise KeyError(key)

	def __call__(cls, value):
		for enum in cls.__enums__:
			try:
				return enum(value)
			except ValueError:
				continue
		raise ValueError(f'{value} is not valid for {cls.__name__}')

	def __or__(cls, other):
		if isinstance(other, EnumType):
			return type(cls)(f'{cls.__name__}|{other.__name__}', dict(), cls.__enums__+[other])
		elif isinstance(other, type(cls)):
			return type(cls)(f'{cls.__name__}|{other.__name__}', dict(), cls.__enums__+other.__enums__)
		raise TypeError('Unsupported type: %s' % type(other))

	def __ior__(cls, other):
		if isinstance(other, EnumType):
			cls.__enums__.append(other)
			return cls
		elif isinstance(other, type(cls)):
			cls.__enums__.extend(other.__enums__)
			return cls
		else:
			raise TypeError('Unsupported type: %s' % type(other))

	__ror__ = __or__

	def values(cls, *values):
		ret = []
		for value in values:
			if isinstance(value, int):
				ret.append(value)
			elif isinstance(value, list):
				ret.extend(value)
			elif isinstance(value, EnumType):
				ret.extend(value._value2member_map_.keys())
			elif isinstance(value, type(cls)):
				for enum in value.__enums__:
					ret.extend(value._value2member_map_.keys())
			elif value is not None:
				raise TypeError('Unexpected type of optional parameter: valuesExpected types: int, list of int, Enum. Given: %s' % type(values))
		for e in cls.__enums__:
			ret.extend(e._value2member_map_.keys())
		return ret


class EnginEnum(Enum):

	@classmethod
	def values(cls, *values):
		ret = []
		for value in values:
			if isinstance(value, int):
				ret = [value]
			elif isinstance(value, list):
				ret.extend(value)
			elif isinstance(value, EnumType):
				ret.extend(value._value2member_map_.keys())
			elif isinstance(value, EnginEnumUnion):
				ret.extend(value.values())
			elif value is not None:
				raise TypeError('Unexpected type of optional parameter: values. Expected types: int, list of int, Enum. Given: ' + type(values))
		ret.extend(cls._value2member_map_.keys())
		return ret

	@classmethod
	def union(cls, *other_events):
		return EnginEnumUnion('Union', {}, other_events+(cls,))


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