import enum
import pdb


class BaseEnum(enum.Enum):

    @classmethod
    def raise_error(cls, error_class, error_message):
        """

        Parameters
        ----------
        error_message : str
            format parameters: class_name, items

        Returns
        -------

        """
        raise error_class(error_message.format(class_name=cls.__name__, items=cls.join(', ')))

    @classmethod
    def join(cls, separator):
        ret = ''
        for name in cls.__members__.keys():
            ret += name + separator
        return ret[:-len(separator)]


class OrientationEnum(BaseEnum):

    VERTICAL = 1
    HORIZONTAL = 2


class TextAlignEnum(BaseEnum):

    LEFT = 1
    CENTER = 2
    RIGHT = 3
