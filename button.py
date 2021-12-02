"""Summary
"""
from typing import Union, Optional, Any, Tuple, List, Iterable, Callable

import pygame

from eventlessbutton import EventlessButton
from modules import Padding, Margin, SizeRange

# pylint: disable=E1101


class Button(EventlessButton):

	"""Summary

	Attributes
	----------
	ID : int
									Description
	BUTTONEVENT : TYPE
									Description
	id : TYPE
									Description
	name : TYPE
									Description
	event : TYPE
									Description
	"""

	BUTTONEVENT = pygame.event.custom_type()

	def __init__(
		self,
		parent,
		pos: Iterable,
		font: Optional[Tuple[str, int, pygame.Color]],
		text: str,
		background: Any,
		text_align: str,
		transparency: bool = False,
		rect_size: Union[pygame.Rect, List[int], Tuple[int, int, int, int]] = None,
		size_range: SizeRange = None,
		padding: Padding = Padding(10),
		borders: Union[int, List[int], Tuple[int, ...]] = 2,
		border_color: Union[pygame.Color, Tuple[int, int, int]] = (255, 255, 255),
		margin: Margin = Margin(0),
		target: Optional[Callable] = None,
	):
		"""Summary

		Parameters
		----------
		parent : pygame.sprite.Sprite
										Description
		pos : Tuple[int, int]
										Description
		font : Union[FontProperty, dict, list, None]
										Description
		text : str
										Description
		background : Tuple[int, int, int]
										Description
		text_align : str
										Description
		trancparency : bool, optional
										Description
		rect_size : Union[list, tuple], optional
										Description
		size_range : SizeRange, optional
										Description
		padding : Padding, optional
										Description
		border : int, optional
										Description
		border_colors : Union[List[int], Tuple[int, int, int]], optional
										Description
		margin : Margin, optional
										Description
		"""
		super().__init__(
			parent,
			pos,
			font,
			text,
			background,
			text_align,
			transparency,
			rect_size,
			size_range,
			padding,
			borders,
			border_color,
			margin,
			target,
		)
		self.event = pygame.event.Event(Button.BUTTONEVENT)
		self.event.button = self
		self.event.button_id = self._id
		self.event.button_name = self.name

	def check_press(self, mouse_event, chenge_curr=False):
		if self.client_rect.collidepoint(mouse_event.pos):
			self.select()
			if (mouse_event.type in 
				(pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP)):
				if self._pressed ^ (mouse_event.type == pygame.MOUSEBUTTONDOWN):
					try:
						self.target()
					except TypeError as er:
						if self.target is not None:
							raise er
					finally:
						self.post()
				self._pressed = mouse_event.type == pygame.MOUSEBUTTONDOWN
			return True
		if not chenge_curr:
			self.unselect()
		self._pressed = False
		return chenge_curr

	def post(self):
		pygame.event.post(self.event)
