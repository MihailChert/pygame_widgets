import pygame

from lable import Lable
from modules import Padding

class Button(Lable):
	ID = 0
	BUTTONEVENT = pygame.event.custom_type()
	def __init__(self, parent, pos, font, text, background, text_align,
				transparency=False, rect_size=None, size_range,
				padding=Padding(10), target=None, singl_active=True):
		super().__init__(parent, pos, font, text, background,
						text_align, transparency, rect_size,
						size_range, padding)
		Lable.ID -= 1
		self.id = Button.ID
		self.name = 'Button' + str(self.id)
		Button.ID += 1
		self.event = pygame.event.Event(Button.BUTTONEVENT)
		self.event.button_id = self.id
		self.event.button_name = self.name
		self.event.target = target
		self.is_ones_activaite = single_active
		self._pressed = False

	@property
	def ispressed(self):
		return self._pressed


	def collide(self, mouse_event):
		if self.rect.collidepoint(mouse_pos):
			if not self.is_ones_activaite or self._pressed^(mouse_event.button == 0):
				pygame.event.post(self.event)
			self._pressed = mouse_event.button == 0

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
		self.background.set_alpha(200)
		self.parent.blit(self.background, self.rect)
		self.background.fill(self.background_color)
		self.draw_text()
