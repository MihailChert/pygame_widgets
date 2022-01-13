from typing import Union, Optional, Any, Tuple, List, Callable

import pygame

from label import Label
from modules import Padding, Margin, SizeRange


class EventlessButton(Label):
    COUNTER = 0
    """Interactive text element.
    On press make target.
    Subclass Label.

    Attributes
    ----------
    COUNTER : int
        Counts all buttons created in program.
    font : modules.FontProperty
        Font of text.
    visible : bool
        Button visibility.
    id : int
        Button's id.
    name : str
        Button's name. Default 'Label{Label.id}.
    parent : pygame.Surface
        The parent surface on which the label is drawn.
    padding : Padding
        Internal indent.
    border : Border
        Button's border.
    margin : Margin
        External indent of button.
    align : str
        Defines the position of text.
    resizable : bool
        Determines whether the size ot the button has been adjusted.
    size_range : SizeRange
        Determines maximum and minimum size. If equal None, then the size depends only on the text
    client_rect : pygame.Rect
        Button's drawing rectangle
    surface : pygame.Surface
        Button's surface. All elements drawing in surface.
    surface_color : pygame.Color.
        Color for text background.
    _active_color: pygame.Color
        The color to be used for drawing interactive object.
    select: function
        Action when hovering the cursor over the object.
    unselect: function
        Action when removing the cursor from the object.
    target: function
        Function has call on pressed.
    """

    def __init__(
            self,
            parent,
            pos: Tuple[int, int],
            font: Optional[Tuple[str, int, pygame.Color]],
            text: str,
            background: Any,
            text_align: str,
            transparency: bool = False,
            rect_size: Union[pygame.Rect, List[int], Tuple[int, int, int, int]] = None,
            size_range: SizeRange = None,
            padding: Padding = Padding(10),
            borders: Union[int, List[int], Tuple[int, ...]] = 2,
            border_color: Union[pygame.Color, Tuple[int, int, int]] = (255, 255, 255),
            margin: Margin = Margin(0),
            target: Optional[Callable] = None,
    ):
        """
        Parameters
        ----------
        parent : pygame.Surface
            The parent surface on which the button is drawn.
        pos : Tuple[int, int]
            Button's position on the parent object.
        font : Union[FontProperty, dict, list, None]
            Button's text font.
        text : str
            Text to write in Button. Text can be multiline.
        background : Tuple[int, int, int]
            Color for text background.
        text_align : str
            Defined text position. Can be center, left, right. Default text align left.
        transparency : bool, optional
            Determines button transparency.
        rect_size : Union[list, tuple], optional
            Button's size. If equal None, then the size of object depends on size range and text.
        size_range : SizeRange, optional
            Determines maximum and minimum size. If equal None, then the size of object depends only on the text.
        padding : Padding, optional
            Internal indent.
        border : int, optional
            Size of label borders.
        border_color : Union[List[int], Tuple[int, int, int]], optional
            Border's color.
        margin : Margin, optional
            External indent. The margins of object add up.
        target : Callable
            Function has call on pressed.
        """
        super().__init__(
            parent,
            pos,
            font,
            text,
            background,
            text_align,
            transparency,
            rect_size,
            size_range,
            padding,
            borders,
            border_color,
            margin,
        )
        Label.COUNTER -= 1
        self.id = EventlessButton.COUNTER
        EventlessButton.COUNTER += 1
        self.target = target
        self._pressed = False
        self.select = self.default_select
        self.unselect = self.default_unselect
        self._active_color = self.surface_color

    @property
    def ispressed(self):
        """Return the status of the button click."""
        return self._pressed

    def default_select(self):
        """Default action when hovering cursor on the button."""
        pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
        self._active_color = pygame.Color(abs(self.surface_color[0] - 40),
                                          abs(self.surface_color[1] - 40),
                                          abs(self.surface_color[2] - 40))

    def default_unselect(self):
        """Default action when remove cursor from the button."""
        pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)
        self._active_color = self.surface_color

    def check_press(self, mouse_event, change_curr=False):
        """Checks whether the mouse pointer is located within the boundaries of the button.
        Parameters
        ----------
        mouse_event : pygame.event.Event
            Mouse event has information about status of mouse.
        change_curr : bool, optional
            The mouse pointer is located within the boundaries of another button.
        Returns
        -------
        bool
            The mouse pointer is located in the button.
        """
        if self.client_rect.collidepoint(mouse_event.pos):
            self.select()
            if mouse_event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
                if self._pressed ^ (mouse_event.type == pygame.MOUSEBUTTONDOWN):
                    try:
                        self.target()
                    except TypeError as er:
                        if self.target is not None:
                            raise er
                self._pressed = mouse_event.type == pygame.MOUSEBUTTONDOWN
            return True
        if not change_curr:
            self.unselect()
        self._pressed = False
        return change_curr

    def draw_pressed(self):
        """Draw button when it is pressed."""
        self.surface.set_alpha(200)

    def draw_unpressed(self):
        """Draw button when it is unpressed."""
        self.surface.set_alpha(255)

    def draw(self):
        """Draw button."""
        if not self.visible:
            return
        try:
            self.parent.blit(self.surface, self.client_rect)
        except AttributeError:
            self.parent.surface.blit(self.surface, self.client_rect)

        self.surface.fill(self._active_color)
        if not self._pressed:
            self.draw_unpressed()
        else:
            self.draw_pressed()
        self.draw_text()
        if hasattr(self.border, 'draw'):
            self.border.draw()
