from typing import Any, Union, Optional, List, Tuple
from math import ceil

import pygame

from modules import Padding, Border, Margin, SizeRange, FontProperty


class Label(pygame.sprite.Sprite):
	default_color = pygame.Color(255, 255, 255)
	COUNTER = 0
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
	"""

	def __init__(
		self,
		parent: pygame.Surface,
		pos: Tuple[int, int],
		font: Union[FontProperty, dict, list, None],
		text: str,
		background: Tuple[int, int, int],
		text_align: str,
		transparency: bool = False,
		rect_size: Union[list, tuple] = None,
		size_range: SizeRange = None,
		padding: Padding = Padding(3),
		border: int = 4,
		border_colors: Union[List[int], Tuple[int, int, int]] = (255, 255, 255),
		margin: Margin = Margin(0),
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
		"""
		pygame.sprite.Sprite.__init__(self)
		self.font = None
		self.set_font(font)
		self.visible = True
		self.id = Label.COUNTER
		self.name = "Label" + str(self.id)
		Label.COUNTER += 1
		self.parent = parent
		self._text = text
		self.padding = padding
		self.border = Border(self, border, border_colors)
		self.margin = margin
		self.align = "l" if text_align is None else text_align.lower()
		self.resizable = rect_size is None
		self.client_rect = pygame.Rect(pos, rect_size if not self.resizable else (0, 0))
		self.size_range = None
		self.set_size_range(size_range)
		if transparency:
			self.surface = pygame.Surface(self.client_rect.size, pygame.SRCALPHA)
		else:
			self.surface = pygame.Surface(self.client_rect.size)
		self.surface.fill(background)
		self.surface_color = background

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
		self.font.create_font()

	def set_rect(self, rect: Union[pygame.Rect, List[int], Tuple[int, ...]]) -> None:
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
		if not isinstance(size_range, (SizeRange, type(None))):
			raise TypeError("Expected type - SizeRange")
		if not self.resizable:
			self.size_range = None
		else:
			self.size_range = size_range
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

	def set_text(self, text: str) -> None:
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
		max_size = [
			0
			if self.size_range is None or self.size_range.min_w is None
			else self.size_range.min_w,
			0
			if self.size_range is None or self.size_range.min_h is None
			else self.size_range.min_h,
		]
		for line in self.text.splitlines():
			if self.size_range is None or self.size_range.max_w is None:
				size = self.font.size(line)[0]
				if max_size[0] < size:
					max_size[0] = size
			elif self.font.size(line)[
				0
			] <= self.size_range.max_w - Padding.absolute_horizontal_indent(
				self.padding, self.border
			):
				size = self.font.size(line)[0]
				if max_size[0] < size:
					max_size[0] = size
			else:
				buffer = []
				line = line.split()
				while len(line) != 0 or self.font.size(" ".join(line))[
					0
				] > self.size_range.max_w - Padding.ansolute_horizontal_indent(
					self.padding, self.border
				):
					while self.font.size(" ".join(line))[
						0
					] > self.size_range.max_w - Padding.absolute_horizontal_indent(
						self.padding, self.border
					):
						buffer.append(line.pop())
					# pdb.set_trace()
					if len(line) == 0:
						raise RuntimeError("Too small rectangle size for text word.")
					size = self.font.size(" ".join(line))[0]
					if max_size[0] < size:
						max_size[0] = size
					line = buffer
					line.reverse()
					buffer = []
					line_counter += 1
				else:
					break
			line_counter += 1
		size = self.font.size("5")[1] * line_counter
		if self.size_range is None or self.size_range.max_h is None:
			if size > max_size[1]:
				max_size[1] = size
		elif size < self.size_range.max_h:
			if size > max_size[1]:
				max_size[1] = size
		else:
			max_size[1] = self.size_range.max_h
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
					- self.padding.rigth
					- self.border.rigth
					- size[0],
					self.padding.top + self.border.top + size[1] * line_number,
				),
				size,
			)
		elif self.align[0] == "c":
			rect = pygame.Rect(
				(
					self.client_rect.w // 2 - size[0] // 2,
					self.padding.top + self.border.top + size[1] * line_number,
				),
				size,
			)
		elif self.align[0] == 'l':
			rect = pygame.Rect(
				(
					self.padding.left + self.border.left,
					self.padding.top + self.border.top + size[1] * line_number,
				),
				size,
			)
		else:
			raise ValueError(f'Unexpected text align: {self.align}.')
		return rect

	def draw_text(self) -> None:
		"""Draw aligned text on surface.
		"""
		line_counter = -1
		for line in self.text.splitlines():
			line_counter += 1
			if self.font.size(line)[
				0
			] <= self.client_rect.width - Padding.absolute_horizontal_indent(
				self.padding, self.border
			):
				render = self.font.render(line, False, self.font.color)
				size = self.font.size(line)
				# pdb.set_trace()
			else:
				buffer = []
				line = line.split()
				while len(line) != 0 or self.font.size(" ".join(line))[
					0
				] > self.client_rect.width - Padding.absolute_horizontal_indent(
					self.padding, self.border
				):
					while self.font.size(" ".join(line))[
						0
					] > self.client_rect.width - Padding.absolute_horizontal_indent(
						self.padding, self.border
					):
						buffer.append(line.pop())
					size = self.font.size(" ".join(line))
					render = self.font.render(" ".join(line), False, self.font.color)
					rect = self.get_rect_align(size, line_counter)
					self.surface.blit(render, rect)
					line = buffer
					line.reverse()
					buffer = []
					line_counter += 1
				render = self.font.render(" ".join(line), False, self.font.color)
				size = self.font.size(" ".join(line))
			rect = self.get_rect_align(size, line_counter)
			self.surface.blit(render, rect)

	def draw(self) -> None:
		"""Draw label on parent"""
		if not self.visible:
			return
		if hasattr(self.parent, 'surface'):
			self.parent.surface.blit(self.surface, self.client_rect)
		else:
			self.parent.blit(self.surface, self.client_rect)
		self.surface.fill(self.surface_color)
		self.draw_text()
		if hasattr(self.border, 'draw'):
			self.border.draw()
