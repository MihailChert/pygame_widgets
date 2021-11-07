import pygame

from lable import Lable
from modules import Padding, Border, Margin

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


	def collide(self, mouse_event, chenge_curr=False):
		if self.rect.collidepoint(mouse_event.pos):
			pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
			if mouse_event.type == pygame.MOUSEBUTTONDOWN or mouse_event.type == pygame.MOUSEBUTTONUP:
				if self._pressed ^ mouse_event.type == pygame.MOUSEBUTTONDOWN:
					pygame.event.post(self.event)
				self._pressed = mouse_event.type == pygame.MOUSEBUTTONDOWN
			return True
		else:
			if not chenge_curr:
				pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)
			self._pressed = False
			return chenge_curr

	def draw(self):
		if not self._pressed:
			self.draw_unpressed()
		else:
			self.draw_pressed()

	def draw_unpressed(self):
		self.surface.set_alpha(255)
		self.parent.blit(self.surface, self.rect)
		self.surface.fill(self.surface_color)
		self.draw_text()

	def draw_pressed(self):
		self.surface.set_alpha(100)
		self.parent.blit(self.surface, self.rect)
		self.surface.fill(self.surface_color)
		self.draw_text()
