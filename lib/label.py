from typing import Any, Union, Optional, List, Tuple
from math import ceil

import pygame
import pdb

from .modules import Padding, Border, Margin, SizeRange, FontProperty
from .objectcheck import ObjectCheck


class Label(pygame.sprite.Sprite, ObjectCheck):
	"""Show static text. Text can change only in program.

	Attributes
	----------
	default_color : pygame.Color
		Default color Label.
	COUNTER : int
		Counts all Labels created in program.
	font : modules.FontProperty
		Font of test.
	visible : bool
		Label visibility.
	id : int
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
	"""

	default_color = pygame.Color(255, 255, 255)
	COUNTER = 0

	def __init__(
		self,
		parent: pygame.Surface,
		pos: Tuple[int, int],
		font: Union[FontProperty, dict, list, None],
		text: str,
		surface_color: Tuple[int, int, int],
		text_align: str,
		transparency: bool = False,
		rect_size: Optional[Union[list, tuple]] = None,
		size_range: Optional[SizeRange] = None,
		padding: Optional[Padding] = Padding(3),
		border: Optional[Border] = 4,
		margin: Optional[Margin] = None,
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
		surface_color : Tuple[int, int, int]
			Color for text background.
		text_align : string
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
		"""
		pygame.sprite.Sprite.__init__(self)
		self.font = None
		self.set_font(font)
		self.visible = True
		self.id = Label.COUNTER
		self.name = (type(self).__name__ + str(self.id))
		Label.COUNTER += 1
		self.parent = parent
		self._text = text
		self.padding = Padding.is_object_exist_else_get_default(padding)
		self.border = Border.is_object_exist_else_get_default(border, parent=self)
		self.margin = Margin.is_object_exist_else_get_default(margin)
		if text_align.lower()[0] not in ['l', 'c', 'r']:
			raise RuntimeError('Unexpected value text align. Use one of list: "right", "center", "left"')
		self.align = text_align.lower()[0]
		self.resizable = rect_size is None
		self.client_rect = pygame.Rect(pos, rect_size if not self.resizable else (0, 0))
		self.size_range = None
		self.set_size_range(size_range)
		self.transparency = transparency
		if transparency:
			self.surface = pygame.Surface(self.client_rect.size, pygame.SRCALPHA)
		else:
			self.surface = pygame.Surface(self.client_rect.size)
		self.surface_color = Border.parse_colors(surface_color)

	def set_font(self, font: Union[FontProperty, dict, list, tuple, None]) -> None:
		"""Set new text font for label.

		Parameters
		----------
		font : Union[FontProperty, dict, list, tuple, None]
			New text font.
		"""
		if isinstance(font, FontProperty):
			self.font = font
		elif isinstance(font, dict):
			self.font = FontProperty(**font)
		elif isinstance(font, (tuple, list)):
			self.font = FontProperty(*font)
		else:
			self.font = FontProperty(None, 16, Label.default_color)

	@property
	def client_rectangle(self) -> pygame.Rect:
		"""
		Returns
		-------
		pygame.Rect
			Rectangle of label.
		"""
		return self.client_rect

	@client_rectangle.setter
	def client_rectangle(self, rect: Union[pygame.Rect, List[int], Tuple[int, ...]]) -> None:
		"""Set new rectangle of object.

		Parameters
		----------
		rect : Union[pygame.Rect, List[int], Tuple[int, ...]]
			New rectangle of object.
		"""
		if isinstance(rect, pygame.Rect):
			self.client_rect = rect
		elif isinstance(rect, (list, tuple)):
			if len(rect) == 4 or len(rect) == 2:
				self.client_rect = pygame.Rect(*rect)
		elif rect is None:
			self.client_rect = self.calc_rect((self.client_rect.x, self.client_rect.y))
			self.resizable = True

	def set_size_range(self, size_range: Optional[SizeRange]) -> None:
		"""Set new size range of object.
		If called without parameters, then the size of the object depends only on the text.

		Parameters
		----------
		size_range : Optional[SizeRange]
			New size range of object.

		Raises
		------
		TypeError
			Expected type - SizeRange
		"""
		# if not isinstance(size_range, SizeRange) or size_range is not None:
		# 	raise TypeError("Unexpected type - SizeRange")
		if not self.resizable:
			self.size_range = SizeRange.is_object_exist_else_get_default(None)
			self.size_range.max_w, self.size_range.max_h = self.client_rect.size
		else:
			self.size_range = SizeRange.is_object_exist_else_get_default(size_range)
			self.client_rect = self.calc_rect((self.client_rect.x, self.client_rect.y))

	@property
	def isresizable(self) -> bool:
		"""Is the size changeable

		Returns
		-------
		bool
			Description
		"""
		return self.resizable

	@property
	def get_rect(self) -> pygame.Rect:
		"""Object's rectangle with external indent.

		Returns
		-------
		pygame.Rect
			Rectangle of object with external indent.
		"""
		return pygame.Rect(
			self.client_rect.x - self.margin.left,
			self.client_rect.y - self.margin.top,
			self.client_rect.width + self.margin.horizontal_indent(),
			self.client_rect.height + self.margin.vertical_indent(),
		)

	@property
	def text(self) -> str:
		"""Text of the label.

		Returns
		-------
		str
			Text of the label
		"""
		return self._text

	@text.setter
	def text(self, text: str) -> None:
		"""Set new text of object.
		if object resizable, then object size recalculate.

		Parameters
		----------
		text : str
			New text.
		"""
		self._text = text
		if self.resizable:
			self.client_rect = self.calc_rect(self.client_rect.topleft)
			self.surface = pygame.Surface(self.client_rect.size)

	def calc_rect(self, pos: Union[List[int], Tuple[int, int]]) -> pygame.Rect:
		"""Calculate size of rectangle.
		Calculate size rectangle on depends on size range and text.

		Parameters
		----------
		pos : Union[List[int], Tuple[int, int]]
			Position of rectangle.

		Returns
		-------
		pygame.Rect
			Rectangle with new size.

		Raises
		------
		RuntimeError
			Too small rectangle size for text word.
		"""
		line_counter = 0
		max_size = [self.size_range.min_w, self.size_range.min_h]

		for line in self.text.splitlines():
			line = line.replace('\t', ' '*4)
			size = self.font.size(line)
			if size[0] <= self.size_range.max_w - Padding.absolute_horizontal_indent(self.padding, self.border):
				if max_size[0] < size[0]:
					max_size[0] = size[0]
				line_counter += 1
				continue
			draw_words_width = 0
			for word in line.replace('\t', ' ').split(' '):
				if draw_words_width <= self.size_range.max_w - Padding.absolute_horizontal_indent(self.padding, self.border):
					draw_words_width += self.font.size(word)[0]
				else:
					if draw_words_width > max_size[0]:
						max_size[0] = draw_words_width
					line_counter += 1
					draw_words_width = 0

		height = self.font.font_size * line_counter
		if height <= (self.size_range.max_h - Padding.absolute_vertical_indent(self.padding, self.border)):
			if max_size[1] < height:
				max_size[1] = height
		else:
			max_size = self.size_range.max_h

		max_size[0] += Padding.absolute_horizontal_indent(self.padding, self.border)
		max_size[1] += Padding.absolute_vertical_indent(self.padding, self.border)
		return pygame.Rect(pos, max_size)

	def moving_intersecting(self, labels: list, movable_x: bool = False, movable_y: bool = False) -> int:
		"""Moving labels intersecting considering margin, padding, border.
		If the offset direction is not selected, the fasted direction is selected.
		Both direction can't be selected. Intersecting objects may remain.

		Parameters
		----------
		labels : List[Label]
			List of labels.
		movable_x : bool, optional
			Direction of move.
		movable_y : bool, optional
			Direction of move.

		Returns
		-------
		int
			Counts of move.
		"""
		self_rect = self.get_rect
		moved = 0
		for label, delta_x, delta_y in Label._collide(self_rect, labels):
			if label is self or label.id == self.id:
				continue
			moved += 1
			if movable_y:
				self._move(label, True, delta_y)
				continue
			if movable_x:
				self._move(label, False, delta_x)
				continue
			axis = delta_x < delta_y
			self._move(label, axis, delta_x if axis else delta_y)
		return moved

	@staticmethod
	def _collide(self_rect: pygame.Rect, collided_labels: list) -> Tuple[Any, int, int]:
		"""Iterate over all stickers intersecting each other.

		Parameters
		----------
		self_rect : pygame.Rect
			Rectangle the object that called moving_intersecting method.
		collided_labels : List[Label]
			Other objects to generate range of intersecting objects.

		Yields
		------
		Tuple[Label, int, int]
			Tuple with intersecting label and deep of intersection.
		"""
		for label in collided_labels:
			if self_rect.colliderect(label.get_rect):
				label_rect = label.get_rect
				delta_x = min(self_rect.w, label_rect.w) - abs(
					self_rect.x - label_rect.x
				)
				delta_y = min(self_rect.h, label_rect.h) - abs(
					self_rect.y - label_rect.y
				)
				yield label, delta_x, delta_y

	def _move(self, label, axis_x: bool, delta):
		"""Both labels move.
		If one of labels near top border, that one do not move.

		Parameters
		----------
		label : Label
			Another movable label
		axis_x : bool
			Direction of move. If move on axis of x, that one equal True, else False
		delta : int
			Distance to move.

		"""
		if axis_x:
			if self.client_rect.x <= label.client_rect.x:
				if self.client_rect.x - ceil(delta / 2) < self.margin.left:
					label.client_rect.x += delta - (self.client_rect.x - self.margin.left)
					self.client_rect.x = self.margin.left
					return
				self.client_rect.x -= ceil(delta / 2)
				label.client_rect.x += ceil(delta / 2)
				return
			if label.client_rect.x - ceil(delta / 2) < label.margin.left:
				self.client_rect.x += delta - (label.client_rect.x - label.margin.left)
				label.client_rect.x = label.margin.left
				return
			self.client_rect.x += ceil(delta / 2)
			label.client_rect.x -= ceil(delta / 2)
			return
		if self.client_rect.y <= label.client_rect.y:
			if self.client_rect.y - ceil(delta / 2) < self.margin.top:
				label.client_rect.y += delta - (self.client_rect.y - self.margin.top)
				self.client_rect.y = self.margin.top
				return
			self.client_rect.y -= ceil(delta / 2)
			label.client_rect.y += ceil(delta / 2)
			return
		if label.client_rect.y - ceil(delta / 2) < label.margin.top:
			self.client_rect.y += delta - (label.client_rect.y - label.margin.top)
			label.client_rect.y = label.margin.top
			return
		self.client_rect.y += ceil(delta / 2)
		label.client_rect.y -= ceil(delta / 2)
		return

	def get_rect_align(self, size: Tuple[int, int], line_number: int) -> pygame.Rect:
		"""Get rectangle to drawing text, depends on text align and line number.
		Text align can be: center - 'c', right - 'r', left - 'l'

		Parameters
		----------
		size : Tuple[int, int]
			Size of drawing text.
		line_number : int
			Number of line to drawing text.

		Returns
		-------
		pygame.Rect
			Rectangle for drawing aligned text.

		Raises
		------
		ValueError
			Unexpected value of text align.
		"""
		if self.align[0] == "r":
			rect = pygame.Rect(
				(
					self.client_rect.w
					- self.padding.right
					- self.border.right
					- size[0],
					self.padding.top + self.border.top + self.font.font_size * line_number + (self.font.font_size - size[1]),
				),
				size,
			)
		elif self.align[0] == "c":
			rect = pygame.Rect(
				(
					self.client_rect.w // 2 - size[0] // 2,
					self.padding.top + self.border.top + self.font.font_size * line_number + (self.font.font_size - size[1]),
				),
				size,
			)
		elif self.align[0] == 'l':
			rect = pygame.Rect(
				(
					self.padding.left + self.border.left,
					self.padding.top + self.border.top + self.font.font_size * line_number + (self.font.font_size - size[1]),
				),
				size,
			)
		else:
			raise ValueError(f'Unexpected text align: {self.align}.')
		return rect

	def draw_text(self):
		"""Draw aligned text on surface."""
		line_counter = 0
		for line in self.text.splitlines():
			line = line.replace('\t', ' '*4)
			size = self.font.size(line)
			if size[0] <= self.client_rect.width - Padding.absolute_horizontal_indent(self.padding, self.border):
				render = self.font.render(line, True, self.font.color)
				self.surface.blit(render, self.get_rect_align(size, line_counter))
				line_counter += 1
				continue
			draw_words_length = 0
			draw_words_width = 0
			for word in line.replace('\t', ' ').split(' '):
				if draw_words_width <= self.client_rect.width - Padding.absolute_horizontal_indent(self.padding, self.border):
					draw_words_length += len(word)
					draw_words_width += self.font.size(word)[0]
				else:
					if draw_words_length == 0:
						raise RuntimeError('Rect calculated wrong')
					render = self.font.render(line[:draw_words_length], True, self.font.color)
					size = (draw_words_width, size[1])
					self.surface.blit(render, self.get_rect_align(size, line_counter))
					line_counter += 1
					line = line[draw_words_length:]
					draw_words_length = 0
					draw_words_width = 0

	def draw(self) -> None:
		"""Draw label on parent"""
		if not self.visible:
			return
		if self.surface.get_size()[0] != self.client_rect.width or self.surface.get_size()[1] != self.client_rect.height:
			if self.transparency:
				self.surface = pygame.Surface(self.client_rect.size, pygame.SRCALPHA)
			else:
				self.surface = pygame.Surface(self.client_rect.size)
		try:
			self.parent.blit(self.surface, self.client_rect)
		except AttributeError:
			self.parent.surface.blit(self.surface, self.client_rect)
		self.surface.fill(self.surface_color)
		self.draw_text()
		if hasattr(self.border, 'draw'):
			self.border.draw(1)
