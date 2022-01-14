import abc


class IEventBound(abc.ABC):

    @abc.abstractmethod
    def post(self):
        """"""

    # noinspection PyDeprecation
    @abc.abstractproperty
    def event(self):
        """"""
