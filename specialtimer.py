from typing import Union, Optional, Callable, List
import threading

import pygame


class TimersController(threading.Thread):
	"""Control Timers on single thread for push event cyclically after a period of time.
	Subclass Thread(daemon)

	Attributes
	----------
	timers : List[Timer]
		All active timers tied with controller.
	"""
	def __init__(self):
		super().__init__(daemon=True)
		self.timers = []
		self.start()

	def start_timer(self, timer: Timer):
		"""Connect timer on timers list.

		Parameters
		----------
		timer : Timer
			Activating timer.
		"""
		self.timers.append(timer)

	def stop_timer(self, timer):
		"""Remove timer from active timers.

		Parameters
		----------
		timer : Timer
			Deactivate timer.
		"""
		self.timers.remov(timer)

	def run(self):
		"""Main body of timer.
		Checks all active timers for the expiration of the interval since the last activation.
		Rewrite method of Thread.
		"""
		while True:
			try:
				for ind, timer in enumerate(self.timers):
					now = pygame.time.get_ticks() - timer._last_activate
					if now >= timer.interval:
						timer.target()
						pygame.event.post(timer.event)
						timer._last_activate = pygame.time.get_ticks()
			except Exception as ex:
				print(ex)
				break


class Timer:
	"""Push event and call target cyclically after a period of time.

	Attributes
	----------
	TIMEREVENT : int
		Event type for pygame.
	COUNTER : int
		Count all timers created in program.
	CONTROLLER : TimersController
		Control  the timer operations.
	interval : int
		Interval of time pause.
	id : int
		Timers id.
	name : str
		Name of timer
	event : pygame.event.Event
		Event pushed of interval end.
	target : Callable
		Function call of interval end.
	"""
	TIMEREVENT = pygame.event.custom_type()
	COUNTER = 0
	CONTROLLER = TimersController()

	def __init__(self, time_interval: int, target: Callable = None, timer_name: str = None):
		"""
		timer_interval : int
			Interval of timer.
		target : Callable
			Function was call of interval end.
		timer_name : str
			Timer's name.
		"""
		self.interval = time_interval
		self.id = Timer.COUNTER
		self._last_activate = None
		Timer.COUNTER += 1
		self.name = 'Timer'+str(self.ID) if timer_name is None else timer_name
		self.event = pygame.event.Event(Timer.TIMEREVENT)
		self.event.timer_id = self.id
		self.event.timer_name = self.name
		self.target = target

	def start(self):
		"""Activate timer."""
		Timer.CONTROLLER.start_timer(self)
		self._last_activate = pygame.time.get_ticks()

	def stop(self):
		"""Stop tomer."""
		Timer.CONTROLLER.stop_timer(self)

	def post(self):
		"""Post event and call target."""
		pygame.event.post(self.event)
		if self.target is not None:
			self.target()
		self._last_activate = pygame.time.get_ticks()
