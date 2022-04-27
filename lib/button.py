from typing import Union, Optional, Tuple, List, Callable

import pygame

from .eventlessbutton import EventlessButton
from .modules import Padding, Margin, SizeRange
from .ieventbound import IEventBound
from .event import Event


class Button(EventlessButton, IEventBound):
	"""Interactive text element.
	On press make target.
	Subclass EventlessButton.

	Attributes
	----------
	BUTTON_EVENT : int
		Event type of button
	COUNTER : int
		Counts all buttons created in program.
	font : modules.FontProperty
		Font of test.
	visible : bool
		Button visibility.
	id : TYPE
		Button's id.
	name : str
		Button's name. Default 'Label{Label.id}.
	parent : pygame.Surface
		The parent surface on which the button is drawn.
	padding : Padding
		Internal indent.
	border : Border
		Button's border.
	margin : Margin
		External indent.
	align : str
		Defines the position of text.
	resizable : bool
		Determines whether the size ot the button has been adjusted.
	client_rect : pygame.Rect
		Button's drawing rectangle
	surface : pygame.Surface
		Button's surface. All elements drawing in surface.
	surface_color : pygame.Color.
		Color for text background.
	size_range : SizeRange
		Determines maximum and minimum size. If equal None, then the size depends only on the text
	event : pygame.event.Event
		Push event on pressed.
	"""

	EVENT_TYPE = Event.custom_type()

	def __init__(
		self,
		parent: pygame.Surface,
		pos: Tuple[int, int],
		font: Optional[Tuple[str, int, pygame.Color]],
		text: str,
		surface_color: pygame.Color,
		text_align: str,
		transparency: bool = False,
		rect_size: Union[pygame.Rect, List[int], Tuple[int, int, int, int]] = None,
		size_range: SizeRange = None,
		padding: Padding = Padding(10),
		border: Union[int, List[int], Tuple[int, ...]] = 2,
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
		surface_color : pygame.Color.
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
		border_color : Union[List[int], Tuple[int, int, int]], optional
			Border's color.
		margin : Margin, optional
			External indent. The margins of object add up.
		target : Callable
			Function has call on pressed. Function must have one parameter.
		"""
		super().__init__(
			parent,
			pos,
			font,
			text,
			surface_color,
			text_align,
			transparency,
			rect_size,
			size_range,
			padding,
			border,
			border_color,
			margin,
			target
		)
		self._event = Event(Button.EVENT_TYPE, button=self, button_id=self.id, button_name=self.name)
		# self._event = pygame.event.Event(Button.BUTTON_EVENT)
		# self.event.button = self
		# self.event.button_id = self.id
		# self.event.button_name = self.name
		self._pressed = False

	@property
	def event(self):
		return self._event

	def check_press(self, mouse_event, change_curr=False):
		if self.client_rect.collidepoint(mouse_event.pos):
			self.select()
			if mouse_event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
				if self._pressed ^ (mouse_event.type == pygame.MOUSEBUTTONDOWN):
					try:
						self.target(self)
					except TypeError as er:
						if self.target is not None:
							raise er
					finally:
						self.post()
				self._pressed = mouse_event.type == pygame.MOUSEBUTTONDOWN
			return True
		if not change_curr:
			self.unselect()
		self._pressed = False
		return change_curr

	def post(self):
		self._event.post()
