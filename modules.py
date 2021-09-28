import pygame

class Padding:
	def __init__(self, padding):
		if isinstance(padding, int):
			padding = [padding]*4
		elif len(padding) < 4:
			if len(padding) == 1:
				padding = padding*4
			elif len(padding) == 2:
				padding = [padding[0], padding[1], padding[0], padding[1]]
		elif len(padding) > 4:
			padding = padding[:4:]
		self.padding = padding

	@property
	def top(self):
		return self.padding[0]
	@property
	def rigth(self):
		return self.padding[1]
	@property
	def bottom(self):
		return self.padding[2]
	@property
	def left(self):
		return self.padding[3]

	def horizontal_indent(self):
		return self.rigth + self.left

	def vertical_indent(self):
		return self.top + self.bottom

class FontProperty:
	def __init__(self, font_name=None, font_size=None, font_color=None):
		self._name = font_name
		self._size = font_size
		self._color = font_color
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
