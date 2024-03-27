import pygame
from enum import EnumMeta
from ..Application.systemevent import EnginEnum
import pdb


class KeyEvent(EnginEnum):

	key_down = pygame.KEYDOWN
	key_up = pygame.KEYUP

	def validate_key(cls, key):
		try:
			if key['name'] is None:
				{}['raise']
			if isinstance(key['name'], str):
				key['name'] = pygame.key.key_code(key['name'])
		except KeyError:
			raise ValueError('KeyEvent mast have name of button')
		return key

class MouseEvent(EnginEnum):

	mouse_move = pygame.MOUSEMOTION
	mouse_key_down = pygame.MOUSEBUTTONDOWN
	mouse_key_up = pygame.MOUSEBUTTONUP
	mouse_wheel = pygame.MOUSEWHEEL

	def validate_key(cls, key):
		cls = type(cls)
		match cls(key['mode']):
			case cls.mouse_wheel:
				if key.get('name', None) is not None:
					raise ValueError('Wheel event have not button')
				key.pop('name', True)
			case cls.mouse_move:
				try:
					if not key.get('name', False) or not key['name'].isdigit():
						key['name'] = None
					if int(key['name']) < 10:
						key['name'] = int(key['name'])
					else:
						raise RuntimeError('The button number is too large, %i more that 10' % key['name'])
				except KeyError:
					pass
				except ValueError:
					raise TypeError('Number of button must be int, not given %s' % type(key['name']))

			case cls.mouse_key_down | cls.mouse_key_up:
				try:
					if int(key['name']) < 10:
						key['name'] = int(key['name'])
					else:
						raise RuntimeError('The button number is too large, %i mare that 10' % key['name'])
				except (KeyError, ValueError):
					raise ValueError('mouse_key_down and mouse_key_up event mast have name of button')

		return key


class JoyEvent(EnginEnum):
	joy_axis_move = pygame.JOYAXISMOTION
	joy_boll_move = pygame.JOYBALLMOTION
	joy_hat_move = pygame.JOYHATMOTION
	joy_key_down = pygame.JOYBUTTONDOWN
	joy_key_up = pygame.JOYBUTTONUP

	def validate_key(cls, key):
		cls = type(cls)
		match cls(key['mode']):
			case cls.joy_key_down | cls.joy_key_up:
				try:
					key['name'] = int(key['name'])
				except (KeyError, ValueError):
					raise ValueError('joy_key_up and joy_key_down event mast have name of the button')

			case cls.joy_hat_move | cls.joy_axis_move | cls.joy_ball_move:
				if key.get('name', None) is not None:
					raise ValueError('joy_hat_move, joy_axis_move and joy_ball_move not have button')
				key.pop('name', True)
		return key
