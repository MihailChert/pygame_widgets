import sys
import pygame


class Event:
    TYPE = pygame.event.custom_type()
    __event_type_counter = 0
    __disabled_event_types = set()

    def __init__(self, event_type, **kwargs):
        self._event = pygame.event.Event(Event.TYPE)
        self._event.event_type = event_type
        self._set_custom_attrs(kwargs)

    # def __getattr__(self, atr):
    #     return getattr(self._event, atr)
    #
    # def __setattr__(self, key, value):
    #     if not hasattr(self._event, key):
    #         raise AttributeError('Unexpected attribute' + key)
    #     setattr(self._event, key, value)

    def _set_custom_attrs(self, custom_args):
        if not isinstance(custom_args, dict):
            raise RuntimeError('Event custom property mast have name.')
        for key, value in custom_args.items():
            if key[0].isdigit():
                raise ValueError('Unexpected name of attribute: ' + key)
            setattr(self._event, key, value)

    def add_custom_attr(self, **kwargs):
        for key, value in kwargs.items():
            if key[0].isdigit():
                raise ValueError('Unexpected name of attribute: ' + key)
            setattr(self._event, key, value)

    def post(self):
        if self._event.event_type in Event.__disabled_event_types:
            return
        pygame.event.post(self._event)

    @staticmethod
    def custom_type():
        Event.__event_type_counter += 1
        return Event.__event_type_counter

    @staticmethod
    def blocked_event_type(event_type):
        Event.__disbled_event_types.add(event_type)

    @staticmethod
    def allove_event_type(event_type):
        Event.__disbled_event_type.discard(event_type)
