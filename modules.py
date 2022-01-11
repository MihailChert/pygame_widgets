"""Summary
"""
from typing import Union, Tuple
from itertools import cycle

import pygame


class Padding:
    """Internal indent of object.

    Attributes
    ----------
    spaces : List[int]
        List of indents of object like padding in css.
    """

    def __init__(self, size_space: Union[int, tuple, list]):
        """
        Parameters
        ----------
        size_space : Union[int, tuple, list]
            Internal indent of object in pixels.

        Raises
        ------
        RuntimeError
            Can't create padding. Length list of spaces must be, 1, 2, 4.
        RuntimeError
            Can't create padding. Spaces must be iterable or int.
        """
        if isinstance(size_space, int):
            self.spaces = [size_space] * 4
        elif isinstance(size_space, (list, tuple)):
            if len(size_space) == 1:
                self.spaces = size_space * 4
            elif len(size_space) == 2:
                self.spaces = [
                    size_space[0],
                    size_space[1],
                    size_space[0],
                    size_space[1],
                ]
            elif len(size_space) == 4:
                self.spaces = size_space
            else:
                raise RuntimeError(f"Can't create '{type(self).__name__}'. Lengths '"
                                   + type(self).__name__ + "' list of spaces must be 1, 2, 4.")
        else:
            raise RuntimeError(
                f"Can't create '{type(self).__name__}'. {type(self).__name__}'s spaces must be iterable or int.")

    def __getattr__(self, name: str) -> tuple:
        """Ability to address on 'spaces' such as 'padding'.

        Parameters
        ----------
        name : str
            Name of attribute.

        Returns
        -------
        tuple
            List of indent.

        Raises
        ------
        AttributeError
            Unexpected attribute.
        """
        if name == "padding":
            return self.spaces
        raise AttributeError(f"Unexpected attribute with name: {name}")

    def __str__(self) -> str:
        """Convert to string.

        Returns
        -------
        str
            String representation.
        """
        return f"top:{self.top}; right:{self.right}; bottom:{self.bottom}; left:{self.left};"

    @property
    def top(self) -> int:
        """Top indent in pixel.

        Returns
        -------
        int
            Top indent.
        """
        return self.spaces[0]

    @property
    def right(self) -> int:
        """Right indent in pixel.

        Returns
        -------
        int
            Right indent.
        """
        return self.spaces[1]

    @property
    def bottom(self) -> int:
        """Bottom indent in pixel.

        Returns
        -------
        int
            Bottom indent.
        """
        return self.spaces[2]

    @property
    def left(self) -> int:
        """Left indent in pixel

        Returns
        -------
        int
            Left indent.
        """
        return self.spaces[3]

    def horizontal_indent(self) -> int:
        """Sum right and left indent.

        Returns
        -------
        int
            Right and left indent.
        """
        return self.rigth + self.left

    def vertical_indent(self) -> int:
        """Sum top and bottom indent.

        Returns
        -------
        int
            Top and bottom indent.
        """
        return self.top + self.bottom

    @staticmethod
    def absolute_vertical_indent(*spaces) -> int:
        """Calculates all vertical indents of object.

        Parameters
        ----------
        *spaces
            Indents of object.

        Returns
        -------
        int
            All vertical indents of object.

        Raises
        ------
        RuntimeError
            Counts of spaces can be 3 or less.
        TypeError
            The object must be class or subclasses of 'Padding'.
        """
        if len(spaces) > 3:
            raise RuntimeError("To mani spaces for the object. Spaces can be 3 or les.")
        res = 0
        for space in spaces:
            if isinstance(space, Padding):
                res += space.top + space.bottom
            else:
                raise TypeError(f"The {type(space)} is not space. It must be class or subclasses of 'Padding'.")
        return res

    @staticmethod
    def absolute_horizontal_indent(*spaces) -> int:
        """Calculates all horizontal indents of object.

        Parameters
        ----------
        *spaces
            Indents of object.

        Returns
        -------
        int
            All horizontal indents of object.

        Raises
        ------
        RuntimeError
            Counts of spaces can be 3 or less.
        TypeError
            The object must be class or subclasses of 'Padding'.
        """
        if len(spaces) > 3:
            raise RuntimeError("To mani spaces for the object. Spaces can be 3 or les.")
        res = 0
        for space in spaces:
            if space is None:
                continue
            if isinstance(space, Padding):
                res += space.left + space.rigth
            else:
                raise TypeError(f"The {type(space)} is not space. It must be class or subclasses of 'Padding'.")
        return res


class Border(Padding):
    """Draw borders of object.
    Subclass to 'Padding'.

    Attributes
    ----------
    spaces : List[int]
        Width lines of border.
    parent : Union[pygame.Surface, pygame.sprite.Sprite]
        The parent surface on which the label is drawn.
    color : pygame.Color.
        Color's lines of border.
    """

    def __init__(
            self,
            parent: Union[pygame.Surface],
            border_widths: Union[int, list, tuple],
            color: Union[list, tuple, pygame.Color]):
        """
        Parameters
        ----------
        parent : Union[pygame.sprite.Sprite, pygame.Surface]
                The parent surface on which the label is drawn.
        border_widths : Union[int, list, tuple]
            Width lines of border.
        color : Union[list, tuple, pygam.Color]
            Color lines of border.

        Raises
        ------
        ValueError
            Parent can't be None
        """
        super().__init__(border_widths)
        if parent is not None:
            self._parent = parent
        else:
            raise ValueError("Parent can't beDescription None")
        for ind, space in enumerate(self.spaces):
            self.spaces[ind] = space * 2
        self.color = Border.parse_colors(color)

    def __getattr__(self, name: str) -> tuple:
        """Ability address to 'spaces' such as 'border'.

        Parameters
        ----------
        name : str
            Attribute name.

        Returns
        -------
        tuple
            Border's width.

        Raises
        ------
        AttributeError
                Unexpected attribute.
        """
        if name == 'border':
            return self.spaces
        raise AttributeError(f"Unexpected attribute with name: {name}")

    def __getitem__(self, key: int):
        """Get border's width by index.

        Parameters
        ----------
        key : int
            Index of border's width.

        Returns
        -------
        tuple
            Border's width and border's color.

        Raises
        ------
        IndexError
            Index out of range. Range 4
        """
        if isinstance(key, int) and -4 <= key < 4:
            if len(self.color) == 3:
                return self.spaces[key], self.color
            return self.spaces[key], self.color
        raise IndexError("Index out of range. Range size 4.")

    def __iter__(self) -> Tuple[int, pygame.Color]:
        """Iteration by border's width and border's color.

        Yields
        ------
        Tuple[int, pygame.Color]
            Border's width and border's color
        """
        for line in self.spaces:
            yield line, self.color

    def __str__(self) -> str:
        """Convert to string.

        Returns
        -------
        str
            String representation.
        """
        return super().__str__() + f" colors:{self.color};"

    @staticmethod
    def parse_colors(color: Union[int, list, tuple, pygame.Color]) -> pygame.Color:
        """Convert color representation to single type rgb.

        Parameters
        ----------
        color : Union[list, tuple]
            Rgb color representation.

        Returns
        -------
        List[Tuple[int, int, int]]
            Color in type pygame.Color.

        Raises
        ------
        TypeError
            Color must be int, list, tuple, pygame.Color
        ValueError
            Length color must be 3(rgb).
        RuntimeError
            Large nesting of the list.
        """
        if isinstance(color, (int, list, tuple, pygame.Color)):
            if isinstance(color, (int, pygame.Color)):
                return pygame.Color(color)
            if len(color) == 3 and isinstance(color[0], int):
                return pygame.Color(color)
            if len(color) == 3 and isinstance(color[0], (list, tuple)):
                raise RuntimeError("Large nesting of the list")
            raise ValueError("Invalid color. Can't create color. Lengths color widths must be 3(rgb)")
        raise TypeError("Colors must be list or tuple.")

    # Generator[YieldType, SendType, ReturnType]
    # pylint: disable = R1708
    def get_border_points(self):
        """Generation rectangle points for drawing lines.

        Yields
        ------
        Tuple[int, int]
            Rectangle points for drawing lines different width.
        """
        switcher = True
        try:
            iter_y = cycle([0, self._parent.client_rectangle.h])
            iter_x = cycle([0, self._parent.client_rectangle.w])
        except AttributeError as ex:
            if isinstance(self._parent, pygame.Surface):
                iter_y = cycle([0, self._parent.get_height()])
                iter_x = cycle([0, self._parent.get_width()])
            else:
                raise ex
        pos_x = next(iter_x)
        pos_y = None
        for _ in range(10):  # limitation loop iterated
            if switcher:
                pos_y = next(iter_y)
            else:
                pos_x = next(iter_x)
            switcher = not switcher
            yield pos_x, pos_y

    # pylint: disable =

    def draw(self) -> None:
        """Draw borders lines on parent."""
        points_iter = self.get_border_points()
        start_point = next(points_iter)
        for line, color in self:
            end_point = next(points_iter)
            if hasattr(self._parent, 'surface'):
                pygame.draw.line(self._parent.surface, color, start_point, end_point, line)
            else:
                pygame.draw.line(self._parent, color, start_point, end_point, line)
            start_point = end_point


class Margin(Padding):
    """External indent of object.
    Subclass  to Padding

    Attributes
    ----------
    spaces : Tuple[int]
        List of indent of object.
    """

    def __getattr__(self, name: str) -> Tuple[int, int, int, int]:
        """Ability address to 'spaces' such as 'margin'.

        Parameters
        ----------
        name : str
            Attribute name.

        Returns
        -------
        Tuple[int, int, int, int]
            Margins indent.

        Raises
        ------
        AttributeError
            Unexpected attribute.
        """
        if name == "margin":
            return self.spaces
        raise AttributeError(f"Unexpected attribute with name: {name}")


class FontProperty:
    """Summary

    Attributes
    ----------
    _name : str

    _size : int

    _color : pygame.Color

    _font: pygame.font.Font
    """

    def __init__(self, font_name: str = None, font_size: int = 16, font_color: Union[int, list, tuple] = 0):
        """
        Parameters
        ----------
        font_name : str, optional
            Name of font. If font equal None, that use default pygame font
        font_size : int, optional
            Size of font. Default equal 16.
        font_color : Union[list, tuple], optional
            Color of font.
        """
        self._name = font_name
        self._size = font_size
        self._color = Border.parse_colors(font_color)
        self._font = None

    def __getattr__(self, name: str):
        """Accessing the attributes of class pygame.font.Font.

        Parameters
        ----------
        name : str
            Name of attribute.

        Returns
        -------
        Callable
            Attribute of class pygame.font.Font
        """
        try:
            return getattr(self._font, name)
        except AttributeError as ex:
            raise ex

    def create_font(self) -> None:
        """Create font of class pygame.font.Font."""
        self._font = pygame.font.Font(self._name, self._size)

    @property
    def font(self) -> pygame.font.Font:
        """Get font of text.

        Returns
        -------
        pygame.font.Font.
            Font of text.
        """
        return self._font

    @property
    def name(self) -> str:
        """Get font name.

        Returns
        -------
        str
            Font name.
        """
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        """Set new font name.
        Rebuild text font.

        Parameters
        ----------
        name : str
            New font name.
        """
        self._name = name
        self.create_font()

    @property
    def size(self) -> int:
        """Get font size.

        Returns
        -------
        int
            Font size.
        """
        return self._size

    @size.setter
    def size(self, size: int):
        """Set new font size.
        Rebuild text font.

        Parameters
        ----------
        size : int
            New font size.

        Raises
        ------
        ValueError
            Size of font must be positive.
        """
        if isinstance(size, int) and size > 0:
            self._size = size
            self.create_font()
        else:
            raise ValueError('Size of font must be positive.')

    @property
    def color(self):
        """Get font color.

        Returns
        -------
        pygame.Color
            Font color.
        """
        return self._color

    @color.setter
    def color(self, color: Union[int, list, tuple, pygame.Color]):
        """Set new Color

        Parameters
        ----------
        color : Union[int, list, tuple pygame.Color]
            New color.
        """
        self._color = Border.parse_colors(color)


class SizeRange:
    """Range of vertical and horizontal size.

    Attributes
    ----------
    range_width : Tuple[int, int]
        Horizontal size range.
    range_height : Tuple[int, int]
        Vertical size range.
    """

    def __init__(self, min_width: int, max_width: int, min_height: int, max_height: int):
        """
        Parameters
        ----------
        min_width : int
            Minimal width.
        max_width : int
            Maximum width.
        min_height : int
            Minimum height
        max_height : int
            Maximum height
        """
        self.range_width = [min_width, max_width]
        self.range_height = [min_height, max_height]

    @property
    def min_w(self) -> int:
        """GEt minimal width.

        Returns
        -------
        int
            Minimum width.
        """
        return self.range_width[0]

    @min_w.setter
    def min_w(self, value: int):
        """Set new minimal width.
        New minimal width must be positive and less maximal width.

        Parameters
        ----------
        value : int
            New minimal width

        Raises
        ------
        ValueError
            New minimal width must be positive and less maximal width.
        """
        if 0 <= value < self.range_width[1] or value is None:
            self.range_width[0] = value
            return
        raise ValueError('Minimal width must be positive and less maximum width.')

    @property
    def max_w(self) -> int:
        """Get maximum width.

        Returns
        -------
        int
            Maximum width.
        """
        return self.range_width[1]

    @max_w.setter
    def max_w(self, value):
        """Set new maximal width.

        Property
        --------
        value : int
            New maximal width.
        Raises
        ------
        ValueError
            Maximal width must be positive and more minimal width.
        """
        if 0 < value and self.range_width[0] < value or value is None:
            self.range_width[1] = value
            return
        raise ValueError('Maximal width must be positive and more minimal width.')

    @property
    def min_h(self) -> int:
        """Get minimal height.

        Returns
        -------
        int
            Minimal height.
        """
        return self.range_height[0]

    @min_h.setter
    def min_h(self, value: int):
        """Set new minimal height.

        Parameters
        ----------
        value : int
            New minimal height

        Raises
        ------
        ValueError
            New minimal height must be positive and less maximal height.
        """
        if 0 <= value < self.range_height[1] or value is None:
            self.range_height[0] = value
            return
        raise ValueError('Minimal width must be positive and less maximum width.')

    @property
    def max_h(self) -> int:
        """Get maximal height.

        Returns
        -------
        int
            Maximal height.
        """
        return self.range_height[1]

    @max_w.setter
    def max_w(self, value):
        """Set new maximal height.

        Property
        --------
        value : int
            New maximal width.
        Raises
        ------
        ValueError
            Maximal width must be positive and more minimal width.
        """
        if 0 < value and self.range_height[0] < value or value is None:
            self.range_height[1] = value
            return
        raise ValueError('Maximal width must be positive and more minimal width.')


if __name__ == '__main__':
    font = FontProperty()
    font.color = pygame.Color(2)
    font.name = 'Times new roman'
    font.size = 25
    print(font.name, font.size)
