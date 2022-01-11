import pygame
import threading
import time


class Timer(threading.Thread):
	COUNTER = 0
	TIMEREVENT = pygame.event.custom_type()
	"""Push event cyclically after a period of time.
	One new timer create new thread.
	Subclass Thread(daemon)

	Attributes
	----------
	COUNTER : id
		Counts all timers created in program.
	TIMEREVENT : int
		Event type of timer.
	active : bool
		Timer is active.
	interval : int
		Interval of time pause.
	name : str
		Name of timer
	id : int
		Timer's id.
	event : pygame.event.Event.
		Event push of interval end.

	"""

	def __init__(self, time_interval: int, timer_name: str = None):
		"""
		Parameters
		----------
		time_interval : int
			Interval of time for push event.
		timer_name : str, optional
			Name of timer
		"""
		super().__init__(daemon=True)
		self.active = False
		self.interval = time_interval
		self.id = Timer.COUNTER
		self.name = timer_name if timer_name is not None else 'Timer' + str(self.id)
		self.event = pygame.event.Event(Timer.TIMEREVENT)
		self.event.timer_id = Timer.COUNTER
		Timer.COUNTER += 1
		self.event.timer = self
		self.event.timer_name = self.name

	def start(self):
		"""Activate timer."""
		if self.active:
			return
		self.active = True
		if not self.is_alive():
			super().start()

	def run(self):
		"""Main body of timer.
		Rewrite method of Thread.
		"""
		while True:
			try:
				if self.active:
					time.sleep(self.interval / 1000)
					pygame.event.post(self.event)
			except Exception as ex:
				print(ex)
				break

	def stop(self):
		"""Timer stop without kill thread."""
		self.active = False


class TargetTimer(Timer):
	"""Push event and call target cyclically after a period of time.
	One new timer create new daemon thread.
	Subclass Timer

	Attributes
	----------
	active : bool
		Timer is active.
	interval : int
		Interval of time pause.
	name : str
		Name of timer
	id : int
		Timer's id.
	event : pygame.event.Event.
		Event pushed of interval end.
	target : Callable.
		Callable object.
	"""

	def __init__(self, time_interval, target, timer_name=None):
		"""
		Parameters
		----------
		time_interval : int
			Interval of time for push event.
		timer_name : str, optional
			Name of timer
		target : Callable
			Function has call on end of interval.
		"""
		super().__init__(time_interval, timer_name)
		self.target = target

	def run(self):
		"""Main body of timer.
		Rewrite method of Thread.
		"""
		while True:
			try:
				if self.active:
					time.sleep(self.interval / 1000)
					self.target()
					pygame.event.post(self.event)
			except Exception as ex:
				print(ex)
				break
