import pdb


class ObjectCheck:
    DEFAULT_VALUES = {}

    @classmethod
    def is_object_exist_else_get_default(cls, obj, **kwargs):
        if not isinstance(obj, cls):
            return cls(**cls.DEFAULT_VALUES)
        return obj

    @classmethod
    def is_objeck_exist(cls, obj):
        if isinstance(obj, cls):
            return obj
        raise TypeError(f'Object not is {cls.__name__}. Object class:{type(obj).__name__}')
