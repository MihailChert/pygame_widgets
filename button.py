from typing import Union, Optional, Any, Tuple, List, Iterable, Callable

import pygame

from label import Label
from modules import Padding, Margin, SizeRange


class Button(Label):

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

	ID = 0
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
		)
		Lable.ID -= 1
		self.id = Button.ID
		self.name = "Button" + str(self.id)
		Button.ID += 1
		self.event = pygame.event.Event(Button.BUTTONEVENT)
		self.event.button = self
		self.event.button_id = self.id
		self.event.button_name = self.name
		self.event.target = target
		self._pressed = False

	@property
	def ispressed(self) -> bool:
		"""Summary

		Returns
		-------
		bool
			Description
		"""
		return self._pressed

	def collide(
		self, mouse_event: pygame.event.Event, chenge_curr: bool = False
	) -> bool:
		"""Summary

		Parameters
		----------
		mouse_event : pygame.event.Event
			Description
		chenge_curr : bool, optional
			Description

		Returns
		-------
		bool
			Description
		"""
		if self.client_rect.collidepoint(mouse_event.pos):
			pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
			if (
				mouse_event.type == pygame.MOUSEBUTTONDOWN
				or mouse_event.type == pygame.MOUSEBUTTONUP
			):
				if self._pressed ^ (mouse_event.type == pygame.MOUSEBUTTONDOWN):
					pygame.event.post(self.event)
				self._pressed = mouse_event.type == pygame.MOUSEBUTTONDOWN
			return True
		if not chenge_curr:
			pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)
		self._pressed = False
		return chenge_curr

	def draw(self) -> None:
		"""Summary"""
		if not self._pressed:
			self.draw_unpressed()
		else:
			self.draw_pressed()

	def draw_unpressed(self) -> None:
		"""Summary"""
		self.surface.set_alpha(255)
		self.parent.blit(self.surface, self.client_rect)
		self.surface.fill(self.surface_color)
		self.draw_text()

	def draw_pressed(self) -> None:
		"""Summary"""
		self.surface.set_alpha(100)
		self.parent.blit(self.surface, self.client_rect)
		self.surface.fill(self.surface_color)
		self.draw_text()
