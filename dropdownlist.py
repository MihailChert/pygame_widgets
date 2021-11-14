import pygame

from button import Button


class DropDownList:
    COUNTER = 0

    def __init__(self, parent, pos, size_range):
        self._id = DropDownList.COUNNTER
        DropDownList.COUNTER += 1


class DropDownListNode(Button):
    def draw_text(self):
        pass
