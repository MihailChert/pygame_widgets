import pygame
import pdb

from itertools import cycle


class Padding:
	def __init__(self, size_space):
		if isinstance(size_space, int):
			size_space = [size_space]*4
		if isinstance(size_space, (list, tuple)):
			if len(size_space) == 1:
				self.spaces = size_space * 4
			elif len(size_space) == 2:
				self.spaces = [size_space[0], size_space[1], size_space[0], size_space[1]]
			elif len(size_space) == 4:
				self.spaces = size_space
			else:
				raise RuntimeError(f'Can\'t create \'{type(self).__name__}\'. Lengths \'{type(self).__name__}\' widths must be 1, 2, 4')
		raise RuntimeError(f'Can\'t create \'{type(self).__name__}\'. {type(self).__name__}\'s widths must be list or tuple')

	def __getattr__(self, name):
		if name == 'padding':
			return self.size_space

	def __str__(self):
		return f'top:{self.top}; rigth:{self.rigth}; bottom:{self.bottom}; left:{self.left};'

	@property
	def top(self):
		return self.size_space[0]
	@property
	def rigth(self):
		return self.size_space[1]
	@property
	def bottom(self):
		return self.size_space[2]
	@property
	def left(self):
		return self.size_space[3]

	def horizontal_indent(self):
		return self.rigth + self.left

	def vertical_indent(self):
		return self.top + self.bottom

class Border(Padding):
	def __init__(self, border_widths, colors, parent):
		super().__init__(border_widths)
		if parent is not None:
			self._parent = parent
		else:
			raise RuntimeError('Parent can\'t be none')
		self.colors = Border.parse_colors(colors)

	def __getattr__(self, name):
		if name == 'widths':
			return self.size_space

	def __getitem__(self, key:int):
		if isinstance(key, int) and key < 4:
			if len(self.colors) == 3:
				return self.size_space[key], self.colors
			else:
				return self.size_space[key], self.colors[key]
		else:
			raise IndexError('Index must be int and les 4')

	def __iter__(self):
		if len(self.colors) == 3:
			for line in self.size_space:
				yield line, self.colors
		else:
			return zip(self.size_space, self.colors)

	def __str__(self):
		return super().__str__() + f' colors:{self.color};'

	@staticmethod
	def parse_colors(colors, rec=0):
		if isinstance(colors, (list, tuple)):
			if len(colors) == 3 and isinstance(colors[0], int):
				return [colors]
			elif len(colors) == 3 and isinstance(colors[0], (list, tuple)):
				raise RuntimeError('Invalid color')
			if isinstance(colors[0], (list, tuple)):
				res = []
				for color in colors:
					res.append(Border.parse_colors(color))
				if len(res) == 1:
					return res[0]
				elif len(res) == 2:
					return [res[0], res[1], res[0], res[1]]
				elif len(res) == 4:
					return res
				else:
					raise RuntimeError('Can\'t create color. Lengths color widths must be 1, 2, 4')
		else:
			raise RuntimeError('Colors must be list or tuple.')

	@property
	def top_color(self):
		if len(self.colors) == 3:
			return self.colors
		else:
			return self.colors[0]
	@property
	def rigth_color(self):
		if len(self.colors) == 3:
			return self.colors
		else:
			return self.colors[1]
	@property
	def bottom_color(self):
		if len(self.colors) == 3:
			return self.colors
		else:
			return self.colors[2]
	@property
	def left_color(self):
		if len(self.colors) == 3:
			return self.colors
		else:
			return self.colors[3]

	def two_line(self, vertical=True):
		if len(self.colors) == 3:
			for line_key in range(int(vertical), int(vartical)+3, 2):
				yield self[line_key]

	def draw(self):
		try:
			margin = self.parent.margin
		except AttributeError:
			margin = Margin(0)
		start_point = None
		counter = 0
		for point in margin.get_border_points():
			if start_point is None:
				start_point = point
				continue
			try:
				width, color = self[counter]
			except IndexError:
				break
			pygame.draw.line(self.parent.background, start_point, point, color, width)
			counter += 1
			start_point = point



class Margin(Padding):
	def __init__(self, margin):
		super().__init__(margin)

	def __getattr__(self, name):
		if name == 'margin':
			return self.size_space

	def get_border_points(self):
		#self.left, self.top 		#3, 0
		#self.rigth, self.top 		#1, 0
		#self.rigth, self.bottom 	#1, 2
		#self.left, self.bottom 	#3, 2
		#self.left, self.top 		#3, 0
		for y in cycle(self.size_space[::2]):
			for x in cycle(self.size_space[-1::-2]):
				yield x, y

class FontProperty:
	def __init__(self, font_name=None, font_size=None, font_color=None):
		self._name = font_name
		self._size = font_size
		self._color = list(font_color)
		self._font = None

	def __getattr__(self, name):
		return getattr(self._font, name)

	def create_font(self):
		self._font = pygame.font.Font(self._name, self._size)

	@property
	def font(self):
		return self._font

	@property
	def font_name(self):
		return self._name
	@font_name.setter
	def set_name(self, name):
		self._name = name
		self.create_font()

	@property
	def font_size(self):
		return self._size
	@font_size.setter
	def set_size(self, size):
		self._size = size
		self.create_font()

	@property
	def color(self):
		return self._color
	@color.setter
	def set_color(self, color):
		self._color = color

class SizeRange:
	def __init__(self, min_width, max_width, min_height, max_height):
		self.range_width = (min_width, max_width)
		self.range_height = (min_height, max_height)

	@property
	def min_w(self):
		return self.range_width[0]
	@property
	def max_w(self):
		return self.range_width[1]
	@property
	def min_h(self):
		return self.range_height[0]
	@property
	def max_h(self):
		return self.range_height[1]

if __name__ == '__main__':
	pygame.font.init()
	font = FontParoperty(None, 35, (0, 0, 4))
	font.create_font()
	print(font.size)
