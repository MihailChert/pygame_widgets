import abc


class IEventBound(abc.ABC):

    @abc.abstractmethod
    def post(self):
        """Publish an event to the event queue for further processing."""

    # noinspection PyDeprecation
    @abc.abstractproperty
    def event(self):
        """Attribute for push on event queue."""
