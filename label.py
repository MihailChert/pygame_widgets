"""Summary
"""
from typing import Any, Union, Optional, List, Tuple, Generator

import pygame

from modules import Padding, Border, Margin, SizeRange, FontProperty


class Label(pygame.sprite.Sprite):

	"""Summary

	Attributes
	----------
	default_color : tuple
			Стандартный цвет метки
	COUNTER : int
			Количество меток в программе
	font : modules.FontProperty
			Шрифт написания текста
	visible : bool
			Отображаемость объекта
	id : TYPE
			Идентификатор метки
	name : str
			Название метки
	parent : pygame.Surface
			Пверхнасть на которой отрисуется объект
	padding : Padding
			Внутренние отступы объекта
	border : Border
			Отрисовывваемая граница объекта
	margin : Margin
			Внешняя граница объекта
	align : str
			Поиционирование текста
	resizble : bool
			Изменяемость размера
	client_rect : pygame.Rect
			Прямоугольник включающий границу, внутренние отступы, содержимое
	surface : pygame.Surface
			Поверхгисть трисовки объекта
	surface_color : pygame.Color
			Цвет поверхности
	size_range : SizeRange
			Минимальные и максимально возможные знчения размеров объекта
	"""

	default_color = (255, 255, 255)
	COUNTER = 0

	def __init__(
		self,
		parent: pygame.sprite.Sprite,
		pos: Tuple[int, int],
		font: Union[FontProperty, dict, list, None],
		text: str,
		background: Tuple[int, int, int],
		text_align: str,
		trancparency: bool = False,
		rect_size: Union[list, tuple] = None,
		size_range: SizeRange = None,
		padding: Padding = Padding(5),
		border: int = 4,
		border_colors: Union[List[int], Tuple[int, int, int]] = (255, 255, 255),
		margin: Margin = Margin(0),
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
		pygame.sprite.Sprite.__init__(self)
		self.font = None
		self.set_font(font)
		self.visible = True
		self._id = Label.COUNTER
		self.name = "Label" + str(self._id)
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
		if trancparency:
			self.surface = pygame.Surface(self.client_rect.size, pygame.SRCALPHA)
		else:
			self.surface = pygame.Surface(self.client_rect.size)
		self.surface_color = background

	def set_font(self, font: Union[FontProperty, dict, list, tuple, None]) -> None:
		"""Summary

		Parameters
		----------
		font : Union[FontProperty, dict, list, tuple, None]
				Description
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

	@property
	def get_id(self):
		return self._id

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

		Returns
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
		self, lables: list, unmovable_x: bool = False, unmovable_y: bool = False
	) -> int:
		"""Смещение наклеек наезжфющих друг на друга учитывая margin, padding
		border

		Parameters
		----------
		lables : List[Label]
				Description
		unmovable_x : bool, optional
				Description
		unmovable_y : bool, optional
				Description

		Returns
		-------
		int
				Description
		"""
		self_rect = self.get_rect
		moved = 0
		for lable, delta_x, delta_y in Label._collide(self_rect, lables):
			moved += 1
			if unmovable_y:
				if self.client_rect.x < lable.client_rect.x:
					self.client_rect.x -= delta_x / 2
					lable.client_rect.x += delta_x / 2
				elif self.client_rect.x > lable.client_rect.x:
					self.client_rect.x += delta_x / 2
					lable.client_rect.x -= delta_x / 2
			elif unmovable_x:
				if self.client_rect.y < lable.client_rect.y:
					self.client_rect -= delta_y / 2
					lable.client_rect.y += delta_y / 2
				elif self.client_rect.y > lable.client_rect.y:
					self.client_rect.y += delta_y / 2
					lable.client_rect.y -= delta_y / 2
			elif delta_x < delta_y:
				if self.client_rect.x < lable.client_rect.x:
					self.client_rect.x -= delta_x / 2
					lable.client_rect.x += delta_x / 2
				elif self.client_rect.x > lable.client_rect.x:
					self.client_rect.x += delta_x / 2
					lable.client_rect.x -= delta_x / 2
			else:
				if self.client_rect.y < lable.client_rect.y:
					self.client_rect -= delta_y / 2
					lable.client_rect.y += delta_y / 2
				elif self.client_rect.y > lable.client_rect.y:
					self.client_rect.y += delta_y / 2
					lable.client_rect.y -= delta_y / 2
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
		collided_lables : List[Label]
				Description

		Yields
		------
		Generator[Label, int, int]
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
		#	 return
		self.parent.blit(self.surface, self.client_rect)
		self.surface.fill(self.surface_color)
		self.draw_text()
		self.border.draw()
