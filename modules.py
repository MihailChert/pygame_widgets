import pygame

from itertools import cycle


class Padding:
	def __init__(self, size_space):
		# pdb.set_trace()
		if isinstance(size_space, int):
			self.spaces = [size_space]*4
		elif isinstance(size_space, (list, tuple)):
			if len(size_space) == 1:
				self.spaces = size_space * 4
			elif len(size_space) == 2:
				self.spaces = [size_space[0], size_space[1], size_space[0], size_space[1]]
			elif len(size_space) == 4:
				self.spaces = size_space
			else:
				raise RuntimeError(f'Can\'t create \'{type(self).__name__}\'. Lengths \'{type(self).__name__}\' widths must be 1, 2, 4')
		else:
			raise RuntimeError(f'Can\'t create \'{type(self).__name__}\'. {type(self).__name__}\'s widths must be list or tuple')

	def __getattr__(self, name):
		if name == 'padding':
			return self.spaces

	def __str__(self):
		return f'top:{self.top}; rigth:{self.rigth}; bottom:{self.bottom}; left:{self.left};'

	@property
	def top(self):
		return self.spaces[0]
	@property
	def rigth(self):
		return self.spaces[1]
	@property
	def bottom(self):
		return self.spaces[2]
	@property
	def left(self):
		return self.spaces[3]

	def horizontal_indent(self):
		return self.rigth + self.left

	def vertical_indent(self):
		return self.top + self.bottom

	@staticmethod
	def absolut_vertical_indent(*spaces):
		if len(spaces) > 3:
			raise RuntimeError('To mani spaces for the object. Can be 3 scpaces or les.')
		res = 0
		for space in spaces:
			if isinstance(space, Padding):
				res += space.top + space.bottom
			else:
				raise RuntimeError(f'The {space} is not space. U can use Padding, Border, Margin')
		return res

	@staticmethod
	def absolute_horizontal_indent(*spaces):
		if len(space) > 3:
			raise RuntimeError('To mani spaces for the object. Can be 3 scpaces or les.')
		res = 0
		for space in spaces:
			if isinstance(space, Padding):
				res += space.left + space.rigth
			else:
				raise RuntimeError(f'The {space} is not space. U can use Padding, Border, Margin')
		return res

class Border(Padding):
	def __init__(self, border_widths, colors, parent):
		# pdb.set_trace()
		super().__init__(border_widths)
		if parent is not None:
			self._parent = parent
		else:
			raise RuntimeError('Parent can\'t be none')
		self.colors = Border.parse_colors(colors)

	def __getattr__(self, name):
		if name == 'widths':
			return self.spaces

	def __getitem__(self, key:int):
		if isinstance(key, int) and key < 4:
			if len(self.colors) == 3:
				return self.spaces[key], self.colors
			else:
				return self.spaces[key], self.colors[key]
		else:
			raise IndexError('Index must be int and les 4')

	def __iter__(self):
		if len(self.colors) == 3:
			for line in self.spaces:
				yield line, self.colors
		else:
			return zip(self.spaces, self.colors)

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
		points_iter = margin.get_border_points()
		start_point = next(points_iter)
		counter = 0
		for line, color in self:
			end_point = next(points_iter)
			pygame.draw.line(self.parent.background, start_point, end_point, color, line)
			start_point = end_point



class Margin(Padding):
	def __init__(self, margin):
		super().__init__(margin)

	def __getattr__(self, name):
		if name == 'margin':
			return self.spaces

	def get_border_points(self):
		#self.left, self.top 		#3, 0
		#self.rigth, self.top 		#1, 0
		#self.rigth, self.bottom 	#1, 2
		#self.left, self.bottom 	#3, 2
		#self.left, self.top 		#3, 0
		switcher = True
		y_iter = cycle(self.spaces[::2])
		x_iter = cycle(self.spaces[-1::-2])
		x = next(x_iter)
		while True:
			if switcher:
				y = next(y_iter)
			else:
				x = next(x_iter)
			yield (x, y)
			switcher = not switcher

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
	import sys
	margin = Margin([0, 1, 2, 3])
	padding = Padding([1, 2])
	marg = Margin(1)
	# m = True
	# print(margin.margin[-1::-2])
	# print(margin.margin[::2])
	# y_iter = cycle(margin.margin[::2])
	# x_iter = cycle(margin.margin[-1::-2])
	# x = next(x_iter)
	# i = 0
	# while i != 5:
	# 	if m:
	# 		y = next(y_iter)
	# 	else:
	# 		x = next(x_iter)
	# 	print(x, y)
	# 	m = not m
	# 	i += 1
	print(margin)
	print(padding)
	print(marg)
	counter = 0
	for x, y in margin.get_border_points():
		print(x, y)
		counter += 1
		if counter == 5:
			break
