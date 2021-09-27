
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
