"""Summary
"""
from typing import Union, NoReturn, Tuple, Generator
from itertools import cycle

import pygame


class Padding:

	"""Summary

	Attributes
	----------
	spaces : TYPE
			Description
	"""

	def __init__(self, size_space: Union[int, tuple, list]) -> NoReturn:
		"""Summary

		Parameters
		----------
		size_space : Union[int, tuple, list]
				Description

		Raises
		------
		RuntimeError
				Description
		"""
		if isinstance(size_space, int):
			self.spaces = [size_space] * 4
		elif isinstance(size_space, (list, tuple)):
			if len(size_space) == 1:
				self.spaces = size_space * 4
			elif len(size_space) == 2:
				self.spaces = [
					size_space[0],
					size_space[1],
					size_space[0],
					size_space[1],
				]
			elif len(size_space) == 4:
				self.spaces = size_space
			else:
				raise RuntimeError(
					f"Can't create '{type(self).__name__}'."
					+ f" Lengths '{type(self).__name__}'"
					+ " widths must be 1, 2, 4"
				)
		else:
			raise RuntimeError(
				f"Can't create '{type(self).__name__}'."
				+ f" {type(self).__name__}'s widths must be list or tuple"
			)

	def __getattr__(self, name: str) -> tuple:
		"""Summary

		Parameters
		----------
		name : str
				Description

		Returns
		-------
		tuple
				Description

		Raises
		------
		AttributeError
				Description
		"""
		if name == "padding":
			return self.spaces
		raise AttributeError(f"Anexpected antribut with name: {name}")

	def __str__(self) -> str:
		"""Summary

		Returns
		-------
		str
				Description
		"""
		return f"top:{self.top}; rigth:{self.rigth}; bottom:{self.bottom}; left:{self.left};"

	@property
	def top(self) -> int:
		"""Summary

		Returns
		-------
		int
				Description
		"""
		return self.spaces[0]

	@property
	def rigth(self) -> int:
		"""Summary

		Returns
		-------
		int
				Description
		"""
		return self.spaces[1]

	@property
	def bottom(self) -> int:
		"""Summary

		Returns
		-------
		int
				Description
		"""
		return self.spaces[2]

	@property
	def left(self) -> int:
		"""Summary

		Returns
		-------
		int
				Description
		"""
		return self.spaces[3]

	def horizontal_indent(self) -> int:
		"""Summary

		Returns
		-------
		int
				Description
		"""
		return self.rigth + self.left

	def vertical_indent(self) -> int:
		"""Summary

		Returns
		-------
		int
				Description
		"""
		return self.top + self.bottom

	@staticmethod
	def absolute_vertical_indent(*spaces) -> int:
		"""Summary

		Parameters
		----------
		*spaces
				Description

		Returns
		-------
		int
				Description

		Raises
		------
		RuntimeError
				Description
		"""
		if len(spaces) > 3:
			raise RuntimeError(
				"To mani spaces for the object. Can be 3 scpaces or les."
			)
		res = 0
		for space in spaces:
			if isinstance(space, Padding):
				res += space.top + space.bottom
			else:
				raise RuntimeError(
					f"The {space} is not space. U can use Padding, Border, Margin"
				)
		return res

	@staticmethod
	def absolute_horizontal_indent(*spaces) -> int:
		"""Summary

		Parameters
		----------
		*spaces
				Description

		Returns
		-------
		int
				Description

		Raises
		------
		RuntimeError
				Description
		"""
		if len(spaces) > 3:
			raise RuntimeError(
				"To mani spaces for the object. Can be 3 scpaces or les."
			)
		res = 0
		for space in spaces:
			if space is None:
				continue
			if isinstance(space, Padding):
				res += space.left + space.rigth
			else:
				raise RuntimeError(
					f"The {space} is not space. U can use Padding, Border, Margin"
				)
		return res


class Border(Padding):

	"""Summary

	Attributes
	----------
	colors : TYPE
			Description
	"""

	def __init__(
		self,
		border_widths: Union[int, list, tuple],
		colors: Union[list, tuple],
		parent: pygame.sprite.Sprite,
	) -> NoReturn:
		"""Summary

		Parameters
		----------
		border_widths : Union[int, list, tuple]
				Description
		colors : Union[list, tuple]
				Description
		parent : pygame.sprite.Sprite
				Description

		Raises
		------
		RuntimeError
				Description
		"""
		super().__init__(border_widths)
		if parent is not None:
			self._parent = parent
		else:
			raise RuntimeError("Parent can't be none")
		for ind, space in enumerate(self.spaces):
			self.spaces[ind] = space * 2
		print(self.spaces)
		self.color = Border.parse_colors(colors)

	def __getattr__(self, name: str) -> tuple:
		"""Summary

		Parameters
		----------
		name : str
				Description

		Returns
		-------
		tuple
				Description

		Raises
		------
		AttributeError
				Description
		"""
		if name == "widths":
			return self.spaces
		raise AttributeError(f"Anexpected antribut with name: {name}")

	def __getitem__(self, key: int) -> tuple:
		"""Summary

		Parameters
		----------
		key : int
				Description

		Returns
		-------
		tuple
				Description

		Raises
		------
		IndexError
				Description
		"""
		if isinstance(key, int) and key < 4:
			if len(self.color) == 3:
				return self.spaces[key], self.color
			return self.spaces[key], self.color[key]
		raise IndexError("Index must be int and les 4")

	def __iter__(self) -> Tuple[int, pygame.Color]:
		"""Summary

		Yields
		------
		tuple
				Description
		"""
		for line in self.spaces:
			yield line, self.color

	def __str__(self) -> str:
		"""Summary

		Returns
		-------
		str
				Description
		"""
		return super().__str__() + f" colors:{self.color};"

	@staticmethod
	def parse_colors(colors: Union[list, tuple]) -> pygame.Color:
		"""Summary

		Parameters
		----------
		colors : Union[list, tuple]
				Description
		rec : int, optional
				Description

		Returns
		-------
		List[Tuple[int, int, int]]
				Description

		Raises
		------
		RuntimeError
				Description
		"""
		if isinstance(colors, (list, tuple, pygame.Color)):
			if len(colors) == 3 and isinstance(colors[0], int):
				return pygame.Color(colors)
			if len(colors) == 3 and isinstance(colors[0], (list, tuple)):
				raise RuntimeError(
					"Invalid color. "
					+ "Can't create color. Lengths color widths must be 3(rgb)"
				)
		raise RuntimeError("Colors must be list or tuple.")

	# Generator[YieldType, SendType, ReturnType]
	# pylint: disable = R1708
	def get_border_points(self) -> Generator[Tuple[int, int], None, None]:
		"""
		Yields
		------
		Generator[Tuple[int, int], None, None]
				Description

		Parameters
		----------
		rect : pygame.Rect
				Description
		"""
		switcher = True
		iter_y = cycle([0, self._parent.client_rectangle.h])
		iter_x = cycle([0, self._parent.client_rectangle.w])
		pos_x = next(iter_x)
		pos_y = None
		for _ in range(10):
			if switcher:
				pos_y = next(iter_y)
			else:
				pos_x = next(iter_x)
			switcher = not switcher
			yield pos_x, pos_y

	# pylint: disable =

	def draw(self) -> None:
		"""Summary"""
		points_iter = self.get_border_points()
		start_point = next(points_iter)
		for line, color in self:
			end_point = next(points_iter)
			pygame.draw.line(self._parent.surface, color, start_point, end_point, line)
			start_point = end_point


class Margin(Padding):

	"""Summary"""

	def __getattr__(self, name: str) -> tuple:
		"""Summary

		Parameters
		----------
		name : str
				Description

		Returns
		-------
		tuple
				Description

		Raises
		------
		AttributeError
				Description
		"""
		if name == "margin":
			return self.spaces
		raise AttributeError(f"Anexpected antribut with name: {name}")


class FontProperty:

	"""Summary"""

	def __init__(
		self,
		font_name: str = None,
		font_size: int = None,
		font_color: Union[list, tuple] = None,
	) -> NoReturn:
		"""Summary

		Parameters
		----------
		font_name : str, optional
				Description
		font_size : int, optional
				Description
		font_color : Union[list, tuple], optional
				Description
		"""
		self._name = font_name
		self._size = font_size
		self._color = list(font_color)
		self._font = None

	def __getattr__(self, name: str):
		"""Summary

		Parameters
		----------
		name : str
				Description

		Returns
		-------
		TYPE
				Description
		"""
		return getattr(self._font, name)

	def create_font(self) -> None:
		"""Summary"""
		self._font = pygame.font.Font(self._name, self._size)

	@property
	def font(self) -> pygame.font.Font:
		"""Summary

		Returns
		-------
		pygame.font.Font
				Description
		"""
		return self._font

	@property
	def font_name(self) -> str:
		"""Summary

		Returns
		-------
		str
				Description
		"""
		return self._name

	@font_name.setter
	def set_name(self, name: str) -> None:
		"""Summary

		Parameters
		----------
		name : str
				Description
		"""
		self._name = name
		self.create_font()

	@property
	def font_size(self) -> int:
		"""Summary

		Returns
		-------
		int
				Description
		"""
		return self._size

	@font_size.setter
	def set_size(self, size: int) -> None:
		"""Summary

		Parameters
		----------
		size : int
				Description
		"""
		self._size = size
		self.create_font()

	@property
	def color(self) -> tuple:
		"""Summary

		Returns
		-------
		tuple
				Description
		"""
		return self._color

	@color.setter
	def set_color(self, color: tuple) -> None:
		"""Summary

		Parameters
		----------
		color : tuple
				Description
		"""
		self._color = color


class SizeRange:

	"""Summary

	Attributes
	----------
	range_width : TYPE
			Description
	range_height : TYPE
			Description
	"""

	def __init__(
		self,
		min_width: int,
		max_width: int,
		min_height: pygame.sprite.Sprite,
		max_height: int,
	) -> NoReturn:
		"""Summary

		Parameters
		----------
		min_width : int
				Description
		max_width : int
				Description
		min_height : pygame.sprite.Sprite
				Description
		max_height : int
				Description
		"""
		self.range_width = (min_width, max_width)
		self.range_height = (min_height, max_height)

	@property
	def min_w(self) -> int:
		"""Summary

		Returns
		-------
		int
				Description
		"""
		return self.range_width[0]

	@property
	def max_w(self) -> int:
		"""Summary

		Returns
		-------
		int
				Description
		"""
		return self.range_width[1]

	@property
	def min_h(self) -> int:
		"""Summary

		Returns
		-------
		int
				Description
		"""
		return self.range_height[0]

	@property
	def max_h(self) -> int:
		"""Summary

		Returns
		-------
		int
				Description
		"""
		return self.range_height[1]
