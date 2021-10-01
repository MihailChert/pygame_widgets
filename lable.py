import numpy
import pygame

from modules import Padding, SizeRange, FontProperty

class Lable(pygame.sprite.Sprite):
	default_color = (255, 255, 255)
	ID = 0

	def __init__(self, parent, pos, font, text,
				background, text_align, trancparency=False, rect_size=None,
				size_range=None, padding=Padding(0)):
		pygame.sprite.Sprite.__init__(self)
		self.font = None
		self.text_font = font
		self.visible = True
		self.id = Lable.ID
		self.name = 'Lable' + str(self.id)
		Lable.ID += 1
		self.parent = parent
		self._text = text
		self.padding = padding
		self.align = 'l' if text_align is None else text_align.lower()
		self.rect_range = size_range
		self.resizble = True
		self.rect = None
		self.rectangle = (pos, rect_size)
		if trancparency:
			self.background = pygame.Surface(self.rect.size, pygame.SRCALPHA)
		else:
			self.background = pygame.Surface(self.rect.size)
		self.background.fill(background)
		self.background_color = background

	@property
	def text_font(self):
		return self.font

	@text_font.setter
	def set_font(self, font):
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
	def recengl(self):
		return self.rect

	@rectangle.setter
	def set_rect(self, rect):
		if isinstance(rect, pygame.Rect):
			self.rect = rect
		elif isinstance(rect, (list, tuple)):
			if len(rect) == 4 or len(rect) == 2:
				self.rect = pygame.Rect(*rect)
		elif rect is None:
			self.rect = self.calc_rect((self.rect.x, self.rect.y))
			self.resizble = True

	@property
	def rect_range(self):
		return self.size_range

	@rect_range.property
	def set_size_range(self, size_range):
		if not isinstance(size_range, SizeRange):
			raise TypeError('Expected type - SizeRange')
		if self.resizble:
			self.size_range = None
		else:
			self.size_range = size_range
			self.rect = self.calc_rect((self.rect.x, self.rect.y))

	@property
	def isresizble(self):
		return self.resizble

	@property
	def text(self):
		return self._text

	def set_text(self, text):
		self._text = text
		if self.resizble:
			self.rect = self.calc_rect(self.rect.topleft)
			self.background = pygame.Surface(self.rect.size)

	def calc_rect(self, pos):
		line_counter = 0
		max_size = [0 if self.size_range is None or self.size_range.min_w is None else self.size_range.min_w,
					0 if self.size_range is None or self.size_range.min_h is None else self.size_range.min_h]
		for line in self.text.splitlines():
			if self.size_range is None or self.size_range.max_w is None:
				size = self.font.size(line)[0]
				if max_size[0] < size:
					max_size[0] = size
			elif self.font.size(line)[0] <= self.size_range.max_w\
				- self.padding.horizontal_indent():
				size = self.font.size(line)[0]
				if max_size[0] < size:
					max_size[0] = size
			else:
				buffer = []
				line = line.split()
				while len(line) != 0\
						or self.font.size(' '.join(line))[0]\
						> self.size_range.max_w\
						- self.padding.horizontal_indent():
					while self.font.size(' '.join(line))[0]\
							> self.size_range.max_w\
							- self.padding.horizontal_indent():
						buffer.append(line.pop())
					# pdb.set_trace()
					size = self.font.size(' '.join(line))[0]
					if max_size[0] < size:
						max_size[0] = size
					line = buffer
					line.reverse()
					buffer = []
					line_counter += 1
				else:
					break
			line_counter += 1
		size = self.font.size('5')[1] * line_counter
		if self.size_range is None or self.size_range.max_h is None:
			if size > max_size[1]:
				max_size[1] = size
		elif size < self.size_range.max_h:
			if size > max_size[1]:
				max_size[1] = size
		else:
			max_size[1] = self.size_range.max_h
		max_size[0] += self.padding.horizontal_indent()
		max_size[1] += self.padding.vertical_indent()
		return pygame.Rect(pos, max_size)

	def get_rect_align(self, size, line_number):

		if self.align[0] == 'r':
			rect = pygame.Rect((self.rect.width-self.padding.rigth-size[0],
								self.padding.top + size[1]*line_number),
								size)
		elif self.align[0] == 'c':
			rect = pygame.Rect((self.rect.w//2 - size[0]//2,
								self.padding.top + size[1]*line_number),
								size)
		else:
			rect = pygame.Rect((self.padding.left,
								self.padding.top+size[1] * line_number),
								size)
		# pdb.set_trace()
		return rect

	def draw_text(self, drawble=True):
		# pdb.set_trace()
		line_counter = -1
		for line in self.text.splitlines():
			line_counter += 1
			if self.font.size(line)[0] <= self.rect.width \
				- self.padding.horizontal_indent():
				render = self.font.render(line, False, self.font.color)
				size = self.font.size(line)
				# pdb.set_trace()
			else:
				buffer = []
				line = line.split()
				while len(line) != 0\
					 or self.font.size(' '.join(line))[0] > self.rect.width\
					 - self.padding.horizontal_indent():
					while self.font.size(' '.join(line))[0] > self.rect.width \
							- self.padding.horizontal_indent():
						buffer.append(line.pop())
					# pdb.set_trace()
					size = self.font.size(' '.join(line))
					render = self.font.render(' '.join(line), False, self.font.color)
					rect = self.get_rect_align(size, line_counter)
					# pdb.set_trace()
					self.background.blit(render, rect)
					line = buffer
					line.reverse()
					buffer = []
					line_counter += 1
				render = self.font.render(' '.join(line), False, self.font.color)
				size = self.font.size(' '.join(line))
			rect = self.get_rect_align(size, line_counter)
			# pdb.set_trace()
			self.background.blit(render, rect)

	def draw(self):
		# pdb.set_trace()
		# if not self.visible:
		# 	return
		self.parent.blit(self.background, self.rect)
		self.background.fill(self.background_color)
		self.draw_text()
