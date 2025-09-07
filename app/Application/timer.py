import pygame
import time
from typing import TypedDict, Optional

class TimeEvent(TypedDict):
	event: pygame.event.Event
	time: float
	loop: Optional[int]
	time_next_push: int

class Timer:

	def __init__(self, app, fps=30):
		self._app = app
		app.update_option('timer', self)
		self.logger = app.get_logger().getChild('Timer')
		self.logger.info('init controller')
		self._events_by_method = list()
		self._event_minimum_time = None
		self._clock = pygame.time.Clock()
		self._fps = None
		self.fps = fps
		self._prev_frame_time = None

	def reset_frame_time(self):
		self._prev_frame_time = None

	def get_frame_time(self):
		if self._prev_frame_time is None:
			self._prev_frame_time = self._clock.tick(self._fps)
			self._push()
		return self._prev_frame_time

	@property
	def fps(self):
		return self._clock.get_fps()

	@fps.setter
	def fps(self, fps):
		if fps <= 0:
			fps = 1000
		self._fps = fps

	def add_event_by_type(self, event, millisecond, loop=1):
		millisecond = int(millisecond)
		if loop is None:
			pygame.time.set_timer(event, millisecond)
		else:
			pygame.time.set_timer(event, millisecond, loop)

	def add_event_by_method(self, event, millisecond, loop=1):
		try:
			event.method
		except AttributeError:
			raise ValueError('Event must have method for the method \'add_event_by_method\'')
		e_by_method: TimeEvent = {
			'event': event,
			'time': millisecond,
			'loop': loop,
			'to_next_push': millisecond
		}
		if millisecond != 0:
			self._events_by_method.append(e_by_method)
			return
		for e in self._events_by_method:
			while e['event'].method == event.method and e in self._events_by_method:
				self._events_by_method.remove(e)

	def _push(self):
		for event in self._events_by_method:
			if event['to_next_push'] - self._prev_frame_time > 0:
				event['to_next_push'] -= self._prev_frame_time
				continue
			
			event['to_next_push'] = event['time'] - (event['to_next_push'] - self._prev_frame_time)
			pygame.event.post(event['event'])
			while event in self._events_by_method and event['loop'] is not None and event['loop'] == 1:
				self._events_by_method.remove(event)
			if event['loop'] is not None:
				event['loop'] -= 1
