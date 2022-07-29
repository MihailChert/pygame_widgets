import pygame

from enum import Enum
from typing import Optional
import warnings

from .modules import Padding, SizeRange, Border
from .ieventbound import IEventBound
from .eventlessbutton import EventlessButton
from .event import Event
from .enumparameters import OrientationEnum


class MenuList(pygame.sprite.Sprite, IEventBound):

    COUNTER = 0
    EVENT_TYPE = Event.custom_type()

    def __init__(
            self,
            parent,
            pos,
            item_size_range: Optional[SizeRange] = None,
            orientation: Enum = OrientationEnum.VERTICAL,
            surface_color=pygame.Color(255),
            item_padding: Padding = Padding((3, 10)),
            padding: Padding = Padding(1),
            border: Border = Border(None, 1, 200)
            ):
        pygame.sprite.Sprite.__init__(self)
        self.visible = True
        self.parent = parent
        self.id = MenuList.COUNTER
        MenuList.COUNTER += 1
        self.name = type(self).__name__ + str(self.id)
        self.items = []
        if not isinstance(orientation, Enum):
            OrientationEnum.raise_error(ValueError, 'Orientation mast be value of enumeration {class_name}: {items}.')
        self.orientation = orientation
        self.item_size_range = SizeRange.is_object_exist_else_get_default(item_size_range)
        self._item_size = [self.item_size_range.min_w, self.item_size_range.min_h]
        self.selected_item_id = False
        self.padding = Padding.is_object_exist_else_get_default(padding)
        self.border = Border.is_object_exist_else_get_default(border, parent=self)
        self.border.set_parent(self)
        self._client_rect = pygame.Rect(pos,
                                        (Padding.absolute_horizontal_indent(self.padding, self.border),
                                         Padding.absolute_vertical_indent(self.padding, self.border)))
        self.item_padding = item_padding
        self.surface = pygame.Surface(self._client_rect.size)
        self.surface_color = surface_color

        self._event = Event(MenuList.EVENT_TYPE, list_name=self.name, list_id=self.id, selected_id=None)

    @property
    def event(self):
        return self._event
    
    @property
    def selected_item(self):
        if not self.selected_item_id:
            return None
        return self.items[self.selected_item_id]

    @property
    def client_rect(self):
        return self._client_rect

    def set_selected_item_id(self, item_id: int):
        if item_id < len(self.items) and isinstance(item_id, int):
            self.selected_item_id = item_id
        else:
            raise RuntimeError(f'Unexpected value in menu list with name {self.name} in items.')

    def change_orientation(self, new_orientation: Enum):
        if not isinstance(new_orientation, Enum):
            raise TypeError('Type of new orientation must be Enum or implemented from Enum.')
        if len(self.items) == 0:
            self.orientation = new_orientation
            return
        if new_orientation == self.orientation:
            return
        try:
            getattr(self, '_change_to_' + self.orientation.name.lower())()
        except AttributeError:
            raise AttributeError('Undefined method for change orientation elements: _change_to' + self.orentation.name.lower())
        except Exception as ex:
            raise ex

    def _change_to_vertical(self):
        for item_, element in enumerate(self.items):
            element.client_rect.y = self.padding.top + self.border.top + self._item_size[1] * item_
            element.client_rect.x = self.padding.left + self.border.left

    def _change_to_horizontal(self):
        for item_, element in enumerate(self.items):
            element.client_rect.y = self.paddindg.top + self.border.top
            element.client_rect.x = self.border.left + self.padding.left + self._item_size[0] * item_

    def add(self, item, index=0):
        if isinstance(item, IEventBound):
            raise RuntimeError('useless post event and haven\'t target')
        if item in self.items:
            warnings.warn('Item already in list')
            return
        self.items.insert(index, item)
        item.parent = self
        item.target = self.create_post
        item.id = len(self.items) - 1
        item.padding = self.item_padding
        item.target = self.create_post
        try:
            getattr(self, '_add_to_' + self.orientation.name.lower())(item)
        except AttributeError:
            raise AttributeError('Undefined method for adding element: _add_to_' + self.orientation.name.lower())
        except Exception as ex:
            raise ex
        self.surface = pygame.Surface(self._client_rect.size)

    def _may_reset_items_rect(self, may_change_size):
        is_reset_size = may_change_size[0] != self._item_size[0]
        is_reset_size = is_reset_size or (may_change_size[1] != self._item_size[1])
        if is_reset_size:
            self._item_size = may_change_size
            for item in self.items:
                item.client_rectangle = pygame.Rect(item.client_rectangle.topleft, may_change_size)
            return True
        return False

    def _add_to_vertical(self, item):
        new_item_size = self._item_size.copy()
        self._client_rect.width = self.item_size_range.get_max_width_from_range([item.client_rect.width, self._item_size[0]])
        new_item_size[0] = self._client_rect.width

        new_item_size[1] = self.item_size_range.get_max_height_from_range([item.client_rect.height, self._item_size[1]])
        item.client_rect.y = self._client_rect.height + self.padding.top + self.border.top
        item.client_rect.x = self.padding.left + self.border.left
        self._client_rect.height += new_item_size[1]
        if not self._may_reset_items_rect(new_item_size):
            item.client_rectangle = pygame.Rect(item.client_rect.topleft, new_item_size)

    def _add_to_horizontal(self, item):
        new_item_size = self._item_size.copy()
        new_item_size[1] = self.item_size_range.get_max_height_from_range([item.client_rect.height, self._item_size[1]])
        self._client_rect.height = new_item_size[1]

        new_item_size[0] = self.item_size_range.get_max_width_from_range([item.client_rect.widht, self._item_size[0]])
        item.client_rect.x = self._client_rect.width + self.padding.left + self.border.left
        item.client_rect.y = self.padding.top + self.border.top
        self._client_rect.width += new_item_size[0]
        if not self._may_reset_items_rect(new_item_size):
            item.client_rectangle = pygame.Rect(item.client_rect.topleft, new_item_size)

    def _remove_from_horizontal(self, count):
        self._client_rect.width -= self._item_size[0] + count
        for iter_, item in enumerate(self.items):
            item.id = iter_
            item.client_rect.x = self._item_size[0] * iter_ + item.margin.left

    def _remove_from_vertical(self, count):
        self._client_rect.height -= self._item_size[1] * count
        for iter_, item in enumerate(self.items):
            item.id = iter_
            item.client_rect.y = self._item_size[1] * iter_ + item.margin.top

    def remove(self, item_id):
        if item_id >= len(self.items):
            raise RuntimeWarning('Index of element out of range elements')
        self.items.pop(item_id)
        try:
            getattr(self, '_remove_from_' + self.orientation.name.lower())(1)
        except AttributeError:
            raise AttributeError('Undefined method for adding element: _remove_from_' + self.orientation.name.lower())
        except Exception as ex:
            raise ex

        self.surface = pygame.Surface(self._client_rect.size)

    def create_post(self, button):
        if not button.ispressed:
            return
        self._event.selected_id = button.id
        self.selected_item_id = button.id
        self.post()

    def post(self):
        self._event.post()

    def check_press(self, mouse_event, change_curr=False):
        if not self._client_rect.collidepoint(mouse_event.pos):
            return change_curr
        for item in self.items:
            change_curr = item.check_press(mouse_event, change_curr)
            if change_curr:
                self.selected_item_id = item.id
        return change_curr

    def draw(self):
        if not self.visible:
            return
        self.surface.fill(self.surface_color)
        self.border.draw()
        for item in self.items:
            item.draw()
        try:
            self.parent.blit(self.surface, self._client_rect)
        except AttributeError:
            self.parent.surface.blit(self.surface, self._client_rect)
