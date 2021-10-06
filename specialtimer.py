import pygame
import threading

class MultiTimer(threading.Thread):
	def __init__(self):
		super().__init__(daemon=True)
		self.timers = []
		self.start()

	def start_timer(self, timer):
		self.timers.append(timer)
		timer._last_activate = pygame.time.get_ticks()

	def stop_timer(self, timer):
		self.timers.remov(timer)

	def run(self):
		while True:
			try:
				for ind, timer in enumerate(self.timers):
					now = pygame.time.get_ticks() - timer._last_activate
					if now >= timer.interval:
						timer._post()
						timer._last_activate = pygame.time.get_ticks()
			except Exception as ex:
				print(ex)
				break


class Timer:
	TIMEREVENT = pygame.event.custom_type()
	ID = 0
	TIMER = MultiTimer()
	def __init__(self, time_interval, target=None, timer_name=None):
		self.interval = time_interval
		self.id = Timer.ID
		self._last_activate = None
		Timer.ID += 1
		self.name = 'Timer'+str(self.ID) if timer_name is None else timer_name
		self.event = pygame.event.Event(Timer.TIMEREVENT)
		self.event.timer_id = self.id
		self.event.timer_name = self.name
		self.event.target = target

	def start(self):
		Timer.TIMER.start_timer(self)
		self.last_activate = pygame.time.get_ticks()

	def stop(self):
		Timer.TIMER.stop_timer(self)

	def _post(self):
		pygame.event.post(self.event)
