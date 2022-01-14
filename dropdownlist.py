import pygame

from modules import FontProperty, Padding
from ieventbound import IEventBound


class DropDownList(pygame.sprite.Sprite, IEventBound):
    COUNTER = 0
    EVENT_ID = pygame.event.custom_type()
    default_font_color = (0, 0, 0)

    def __init__(
        self,
        parent,
        font,
        pos,
        beckground_color=(255, 255, 255),
        item_padding=Padding(10),
        max_width=0,
    ):
        pygame.sprite.Sprite.__init__(self)
        self.visible = True
        self._id = DropDownList.COUNNTER
        DropDownList.COUNTER += 1
        self.set_font(font)
        self.name = "DropDownList" + str(self._id)
        self.item_size = item_size
        self.items = []
        self.selected_item = None
        self._event = DropDownList._create_event()
        self.rect = pygame.Rect(pos, (0, 0))
        self.max_width = max_width
        self.surface = pygame.Surface()
        self.surface_color = beckground_color

    @property
    def event(self):
        return self._event

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

    def _create_event(self):
        if self._event is not None:
            return self._event
        event = pygame.event.Event(DropDownList.EVENT_ID)
        event.list_name = self.name
        event.list_id = self._id
        event.item_id = None
        return event

    def add_item(self, item_name, item_width=0):
        self.items.append(item_name)
        self.rect.h += self.font.get_height() + self.item_padding.vertical_indent()
        self.rect.w = max(item_width, self.font.size(item_name)[0], self.rect.width)
        if 0 < self.max_width < self.rect.width:
            self.rect.width = self.max_width
        self.draw()

    def draw(self):
        if self.visible:
            pass
