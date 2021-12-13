from typing import Union, Optional, Any, Tuple, List, Iterable, Callable

import pygame

from label import Label
from modules import Padding, Margin, SizeRange


class Button(Label):

	"""Interactive text element.
	On press make target.
	Subclass Label.

	Attributes
	----------
	BUTTONEVENT : int
		Event type of button
	COUNTER : int
		Counts all Labels created in program.
	font : modules.FontProperty
		Font of test.
	visible : bool
		Label visibility.
	id : TYPE
		Label's id.
	name : str
		Label's name. Default 'Label{Label.id}.
	parent : pygame.Surface
		The parent surface on which the label is drawn.
	padding : Padding
		Internal indent.
	border : Border
		Label's border.
	margin : Margin
		External indent.
	align : str
		Defines the position of text.
	resizable : bool
		Determines whether the size ot the label has been adjusted.
	client_rect : pygame.Rect
		Label's drawing rectangle
	surface : pygame.Surface
		Label's surface. All elements drawing in surface.
	surface_color : pygame.Color.
		Color for text background.
	size_range : SizeRange
		Determines maximum and minimum size. If equal None, then the size depends only on the text
	event : TYPE
		Push event on pressed.
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
		"""
		Parameters
		----------
		parent : pygame.Surface
			The parent surface on which the label is drawn.
		pos : Tuple[int, int]
			Label's position on the parent object.
		font : Union[FontProperty, dict, list, None]
			Label's text font.
		text : str
			Text to write in label. Text can be multiline.
		background : Tuple[int, int, int]
			Color for text background.
		text_align : str
			Defined text position. Can be center, left, right. Default text align left.
		transparency : bool, optional
			Determines label transparency.
		rect_size : Union[list, tuple], optional
			Label's size. If equal None, then the size of object depends on size range and text.
		size_range : SizeRange, optional
			Determines maximum and minimum size. If equal None, then the size of object depends only on the text.
		padding : Padding, optional
			Internal indent.
		border : int, optional
			Size of label borders.
		border_colors : Union[List[int], Tuple[int, int, int]], optional
			Border's color.
		margin : Margin, optional
			External indent. The margins of object add up.
		target : Callable
			Function has active on pressed.
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
		"""Get status of button.

		Returns
		-------
		bool
			Button pressed
		"""
		return self._pressed

	def collide(self, mouse_event: pygame.event.Event, change_curr: bool = False) -> bool:
		"""Checks whether the mouse pointer is located within the boundaries of the button.

		Parameters
		----------
		mouse_event : pygame.event.Event
			Mouse event has information about status of mouse.
		change_curr : bool, optional
			The mouse pointer is located within the boundaries of another button.

		Returns
		-------
		bool
			The mouse pointer is located in the button.
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
		if not change_curr:
			pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)
		self._pressed = False
		return change_curr

	def draw(self) -> None:
		"""Draw button on parent surface."""
		if not self._pressed:
			self.draw_unpressed()
		else:
			self.draw_pressed()

	def draw_unpressed(self) -> None:
		"""Draw button when it is unpressed."""
		self.surface.set_alpha(255)
		if hasattr(self.parent, 'surface'):
			self.parent.surface.blit(self.surface, self.client_rect)
		else:
			self.parent.blit(self.surface, self.client_rect)
		self.surface.fill(self.surface_color)
		self.draw_text()

	def draw_pressed(self) -> None:
		"""Draw button when it is pressed"""
		self.surface.set_alpha(100)
		if hasattr(self.parent, 'surface'):
			self.parent.surface.blit(self.surface, self.client_rect)
		else:
			self.parent.blit(self.surface, self.client_rect)
		self.surface.fill(self.surface_color)
		self.draw_text()
