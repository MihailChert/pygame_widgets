from typing import Any, Union, Optional, List, Tuple, Generator
from math import ceil

import pygame

from modules import Padding, Border, Margin, SizeRange, FontProperty


class Label(pygame.sprite.Sprite):

	"""Show statik text. Text can change in program.

	Attributes
	----------
	default_color : pygame.Color
		Default color Label.
	COUNTER : int
		Count all Labels created in program.
	font : modules.FontProperty
		Font of test.
	visible : bool
		Label's visible.
	id : TYPE
		Label's id.
	name : str
		Label's name. Default 'Label{Label.id}.
	parent : pygame.Surface
		Пверхнасть на которой отрисуется объект
	padding : Padding
		Label's padding.
	border : Border
		Label's border.
	margin : Margin
		Label's margin.
	align : str
		Defined text position.
	resizble : bool
		Defined fixed label size
	client_rect : pygame.Rect
		Label's drawing rectangle
	surface : pygame.Surface
		Label's surface. All elements drawing in surface.
	surface_color : pygame.Color.
		Color for text background.
	size_range : SizeRange
		Defined maximum and minimum size.
	"""

	default_color = pygame.Color(255, 255, 255)
	COUNTER = 0

	def __init__(
		self,
		parent: pygame.sprite.Sprite,
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
		parent : pygame.sprite.Sprite
			Description
		pos : Tuple[int, int]
			Label's position on parent.
		font : Union[FontProperty, dict, list, None]
			Label's text font.
		text : str
			Text to write in label
		background : Tuple[int, int, int]
			Color for text background.
		text_align : str
			Defined text position.
		transparency : bool, optional
			Defined label transparency.
		rect_size : Union[list, tuple], optional
			Label's size.
		size_range : SizeRange, optional
			Defined maximum and minimum size.
		padding : Padding, optional
			Label's padding.
		border : int, optional
			Label's border.
		border_colors : Union[List[int], Tuple[int, int, int]], optional
			Border's color.
		margin : Margin, optional
			Label's margin.
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
		self.border = Border(border, border_colors, self)
		self.margin = margin
		self.align = "l" if text_align is None else text_align.lower()
		self.resizble = rect_size is None
		self.client_rect = pygame.Rect(pos, rect_size if not self.resizble else (0, 0))
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
			self.font = FontProperty(None, 16, Lable.default_color)
		self.font.create_font()

	@property
	def client_rectangle(self) -> pygame.Rect:
		"""Summary

		Returns
		-------
		pygame.Rect
			Description
		"""
		return self.client_rect

	@client_rectangle.setter
	def set_rect(self, rect: Union[pygame.Rect, List[int], Tuple[int, ...]]) -> None:
		"""Summary

		Parameters
		----------
		rect : Union[pygame.Rect, List[int], Tuple[int, ...]]
			Description
		"""
		if isinstance(rect, pygame.Rect):
			self.client_rect = rect
		elif isinstance(rect, (list, tuple)):
			if len(rect) == 4 or len(rect) == 2:
				self.client_rect = pygame.Rect(*rect)
		elif rect is None:
			self.client_rect = self.calc_rect((self.client_rect.x, self.client_rect.y))
			self.resizble = True

	def set_size_range(self, size_range: Optional[SizeRange]) -> None:
		"""Summary

		Parameters
		----------
		size_range : Optional[SizeRange]
			Description

		Raises
		------
		TypeError
			Description
		"""
		if not isinstance(size_range, (SizeRange, type(None))):
			raise TypeError("Expected type - SizeRange")
		if not self.resizble:
			self.size_range = None
		else:
			self.size_range = size_range
			self.client_rect = self.calc_rect((self.client_rect.x, self.client_rect.y))

	@property
	def isresizble(self) -> bool:
		"""Summary

		Returns
		-------
		bool
			Description
		"""
		return self.resizble

	@property
	def get_rect(self) -> pygame.Rect:
		"""Summary

		Returnsi
		-------
		pygame.Rect
			Description
		"""
		return pygame.Rect(
			self.client_rect.x - self.margin.left,
			self.client_rect.y - self.margin.top,
			self.client_rect.width + self.margin.horizontal_indent(),
			self.client_rect.height + self.margin.vertical_indent(),
		)

	@property
	def text(self) -> str:
		"""Summary

		Returns
		-------
		str
			Description
		"""
		return self._text

	def set_text(self, text: str) -> None:
		"""Summary

		Parameters
		----------
		text : str
			Description
		"""
		self._text = text
		if self.resizble:
			self.client_rect = self.calc_rect(self.client_rect.topleft)
			self.surface = pygame.Surface(self.client_rect.size)

	def calc_rect(self, pos: Union[List[int], Tuple[int, int]]) -> pygame.Rect:
		"""Summary

		Parameters
		----------
		pos : Union[List[int], Tuple[int, int]]
			Description

		Returns
		-------
		pygame.Rect
			Description

		Raises
		------
		RuntimeWarning
			Description
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

	def calculate_collide(
		self, labels: list, movable_x: bool = False, movable_y: bool = False
	) -> int:
		"""Смещение наклеек наезжфющих друг на друга учитывая margin, padding
		border

		Parameters
		----------
		lables : List[Lable]
			Description
		movable_x : bool, optional
			Description
		movable_y : bool, optional
			Description

		Returns
		-------
		int
			Description
		"""
		self_rect = self.get_rect
		moved = 0
		for label, delta_x, delta_y in Label._collide(self_rect, labels):
			if label is self or label.id == self.id:
				continue
			moved += 1
			if movable_y:
				self._move(label, True, delta_x)
				continue
			if movable_x:
				unmove = self._move(label, False, delta_y)
				continue
			axis = delta_x < delta_y
			self._move(label, axis, delta_x if axis else delta_y)
		return moved

	@staticmethod
	def _collide(
		self_rect: pygame.Rect, collided_lables: list
	) -> Generator[Any, int, int]:
		"""Итерация по всем наклейкам пересекающих друг друга, возвращает метку и разницу

		Parameters
		----------
		self_rect : pygame.Rect
			Description
		collided_lables : List[Lable]
			Description

		Yields
		------
		Generator[Lable, int, int]
			Description
		"""
		for lable in collided_lables:
			if self_rect.colliderect(lable.get_rect):
				lable_rect = lable.get_rect
				delta_x = min(self_rect.w, lable_rect.w) - abs(
					self_rect.x - lable_rect.x
				)
				delta_y = min(self_rect.h, lable_rect.h) - abs(
					self_rect.y - lable_rect.y
				)
				yield lable, delta_x, delta_y
				
	def _move(self, label, axis_x:bool, delta):
		if axis_x:
			if self.client_rect.x <= lable.client_rect.x:
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
		"""Summary

		Parameters
		----------
		size : Tuple[int, int]
			Description
		line_number : int
			Description

		Returns
		-------
		pygame.Rect
			Description
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
		else:
			rect = pygame.Rect(
				(
					self.padding.left + self.border.left,
					self.padding.top + self.border.top + size[1] * line_number,
				),
				size,
			)
		# pdb.set_trace()
		return rect

	def draw_text(self) -> None:
		"""Summary

		Parameters
		----------
		drawble : bool, optional
			Description
		"""
		# pdb.set_trace()
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
					# pdb.set_trace()
					size = self.font.size(" ".join(line))
					render = self.font.render(" ".join(line), False, self.font.color)
					rect = self.get_rect_align(size, line_counter)
					# pdb.set_trace()
					self.surface.blit(render, rect)
					line = buffer
					line.reverse()
					buffer = []
					line_counter += 1
				render = self.font.render(" ".join(line), False, self.font.color)
				size = self.font.size(" ".join(line))
			rect = self.get_rect_align(size, line_counter)
			# pdb.set_trace()
			self.surface.blit(render, rect)

	def draw(self) -> None:
		"""Summary"""
		# pdb.set_trace()
		# if not self.visible:
		# 	return
		self.parent.blit(self.surface, self.client_rect)
		self.surface.fill(self.surface_color)
		self.draw_text()
		self.border.draw()
