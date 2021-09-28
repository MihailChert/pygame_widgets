import numpy
import pdb
import pygame

from modules import Padding, SizeRange, FontProperty

class Lable(pygame.sprite.Sprite):
	default_color = (255, 255, 255)

	def __init__(self, parent, pos, font, text,
				background, text_align, trancparency=False, rect_size=None,
				size_range=None, padding=Padding(0)):
		pygame.sprite.Sprite.__init__(self)
		if isinstance(font, FontProperty):
			self.font = font
		elif isinstance(font, dict):
			self.font = FontProperty(**font)
		elif isinstance(font, (tuple, list)):
			self.font = FontProperty(*font)
		else:
			self.font = FontProperty(None, 16, Lable.default_color)
		self.font.create_font()
		self.visible = True
		self.parent = parent
		self._text = text
		self.padding = padding
		self.align = 'l' if text_align is None else text_align.lower()
		if rect_size is not None:
			self.size_range = None
			self.resizble = False
			self.rect = pygame.Rect(pos, rect_size)
		elif size_range is not None:
			self.size_range = size_range
			self.resizble = True
			self.rect = self.calc_rect(pos)
		else:
			self.size_range = None
			self.resizble = True
			self.rect = self.calc_rect(pos)
		if trancparency:
			self.background = pygame.Surface(self.rect.size, pygame.SRCALPHA)
		else:
			self.background = pygame.Surface(self.rect.size)
		self.background.fill(background)
		self.background_color = background

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
		max_size = [0 if self.size_range is None else self.size_range.min_w,
					0 if self.size_range is None else self.size_range.min_h]
		for line in self.text.split('\n'):
			line_counter += 1
			if self.size_range is None or self.size_range.max_w is None:
				size = self.font.size(line)[0]
				if max_size[0] < size:
					max_size[0] = size
			elif self.font.size(line)[0] < self.size_range.max_w\
				- self.padding.horizontal_indent():
				size = self.font.size(line)[0]
				if max_size[0] < size:
					max_size[0] = size
			else:
				buffer = []
				line = line.split(' ')
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
		for line in self.text.split('\n'):
			line_counter += 1
			if self.font.size(line)[0] < self.rect.width \
				- self.padding.horizontal_indent():
				render = self.font.render(line, False, self.font.color)
				size = self.font.size(line)
			else:
				buffer = []
				line = line.split(' ')
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
					self.background.blit(render, rect)
					line = buffer
					line.reverse()
					buffer = []
					line_counter += 1
				render = self.font.render(' '.join(line), False, self.font.color)
				size = self.font.size(' '.join(line))
			rect = self.get_rect_align(size, line_counter)
			self.background.blit(render, rect)

	def draw(self):
		# pdb.set_trace()
		# if not self.visible:
		# 	return
		self.parent.blit(self.background, self.rect)
		self.background.fill(self.background_color)
		self.draw_text()
