import pygame

from modules import FontProperty, Padding


class DropDownList(pygame.sprite.Sprite):
	COUNTER = 0
	EVENT_ID = pygame.event.custom_type()
	default_font_color = (0, 0, 0)

	def __init__(self, parent, font, pos, beckground_color=(255, 255, 255),
				item_padding=Padding(10)):
		pygame.sprite.Sprite.__init__(self)
		self._id = DropDownList.COUNNTER
		DropDownList.COUNTER += 1
		self.set_font(font)
		self.name = 'DropDownList' + str(self._id)
		self.item_size = item_size
		self.items = []
		self._event = DropDownList._create_event()
		self.rect = pygame.Rect(pos, (0, 0))
		self.surface = pygame.Surface()
		self.surface_color = beckground_color

	def set_font(self, font):
		if isinstance(font, FontProperty):
			self.font = font
		elif isinstance(font, dict):
			self.font = FontProperty(**font)
		elif isinstance(font, (tuple, list)):
			self.font = FontProperty(*font)
		else:
			self.font = FontProperty(None, 16, DropDownList.default_font_color)
		self.font.create_font()

	@statikmethod
	def _create_event():

	def add_item(self, item_name, item_size=(0, 0)):
		self.items.append(item_name)
		self.rect.h += self.item_size.h
		self.rect.w = max(self.item_size)
		self.draw()

	def draw(self):

