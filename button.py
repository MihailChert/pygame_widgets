import pygame
import pdb

from lable import Lable
from modules import Padding

class Button(Lable):
	ID = 0
	BUTTONEVENT = pygame.event.custom_type()

	def __init__(self, parent, pos, font, text, background, text_align,
				transparency=False, rect_size=None, size_range=None,
				padding=Padding(10), target=None):
		super().__init__(parent, pos, font, text, background,
						text_align, transparency, rect_size,
						size_range, padding)
		Lable.ID -= 1
		self.id = Button.ID
		self.name = 'Button' + str(self.id)
		Button.ID += 1
		self.event = pygame.event.Event(Button.BUTTONEVENT)
		self.event.button = self
		self.event.button_id = self.id
		self.event.button_name = self.name
		self.event.target = target
		self._pressed = False

	@property
	def ispressed(self):
		return self._pressed


	def collide(self, mouse_event):
		if mouse_event.button == 1:
			if self.rect.collidepoint(mouse_event.pos):
				if self._pressed ^ mouse_event.type == pygame.MOUSEBUTTONDOWN:
					pygame.event.post(self.event)
				self._pressed = mouse_event.type == pygame.MOUSEBUTTONDOWN
			else:
				self._pressed = False

	def draw(self):
		if not self._pressed:
			self.draw_unpressed()
		else:
			self.draw_pressed()

	def draw_unpressed(self):
		self.background.set_alpha(255)
		self.parent.blit(self.background, self.rect)
		self.background.fill(self.background_color)
		self.draw_text()

	def draw_pressed(self):
		self.background.set_alpha(100)
		self.parent.blit(self.background, self.rect)
		self.background.fill(self.background_color)
		self.draw_text()
