import pygame
import pdb

from modules import FontProperty, Padding
from ieventbound import IEventBound


class DropDownList(pygame.sprite.Sprite, IEventBound):
    COUNTER = 0
    DROPDOWNLISTEVENT = pygame.event.custom_type()

    def __init__(self,
                 parent,
                 pos,
                 item_height,
                 surface_color=(255, 255, 255),
                 max_width=0,
                 item_padding: Padding = Padding((3, 10))
                 ):
        pygame.sprite.Sprite.__init__(self)
        self.visible = True
        self.parent = parent
        self._id = DropDownList.COUNTER
        DropDownList.COUNTER += 1
        self.name = type(self).__name__ + str(self._id)
        self.items = []
        self.selected_item = None
        self.client_rect = pygame.Rect(pos, (0, 0))
        self.max_width = max_width
        self.item_height = item_height
        self.item_padding = item_padding
        self.surface = pygame.Surface(self.client_rect.size)
        self.surface_color = surface_color

        self.event = pygame.event.Event(DropDownList.DROPDOWNLISTEVENT)
        self.event.list_name = self.name
        self.event.list_id = self._id
        self.event.selected_id = None

    def add_item(self, item):
        if (hasattr(item, 'event') or hasattr(item, 'post')) and not hasattr(item, 'target'):
            raise RuntimeError('useless post event and haven\'t target')
        self.items.append(item)
        item.parent = self
        item.target = self.post
        item.id = len(self.items)
        self.client_rect.width = max(item.client_rect.width, self.client_rect.width)
        if 0 < self.max_width < self.client_rect.width:
            self.client_rect.width = self.max_width
        for iter, elem in enumerate(self.items):
            elem.client_rect.width = self.client_rect.width
        item.padding = self.item_padding
        item.client_rect.y = self.client_rect.height
        self.client_rect.height += self.item_height
        self.surface = pygame.Surface(self.client_rect.size)

    def remove_item(self, item):
        self.items.remove(item)
        self.client_rect.height -= self.item_height
        for iter, elem in enumerate(self.items):
            elem.client_rect.pos = (0, iter * self.item_height)
            elem.id = iter
        self.surface = pygame.Surface(self.client_rect.size)

    def post(self, button):
        print(button.client_rect)
        self.event.selected_id = self.selected_item = button.id
        pygame.event.post(self.event)

    def check_press(self, mouse_event, change_curr=False):
        for item in self.items:
            change_curr = item.check_press(mouse_event, change_curr)
        return change_curr

    def draw(self):
        if not self.visible:
            return
        try:
            self.parent.blit(self.surface, self.client_rect)
        except AttributeError:
            self.parent.surface.blit(self.surface, self.client_rect)
        self.surface.fill(self.surface_color)
        for item in self.items:
            item.draw()
