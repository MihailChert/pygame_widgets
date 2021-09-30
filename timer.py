import pygame
import threading
import time, pdb


class Timer(threading.Thread):
	TIMEREVENT = pygame.event.custom_type()
	def __init__(self, timer_id, time_interval, timer_name=None):
		super().__init__(daemon=True)
		self.active = False
		self.interval = time_interval
		self.event = pygame.event.Event(Timer.TIMEREVENT)
		self.event.timer_id = timer_id
		self.event.timer = self
		self.event.name = timer_name if timer_name is not None else f'Timer{timer_id}'

	def start(self):
		# pdb.set_trace()
		if self.active:
			return
		self.active = True
		if not self.is_alive():
			super().start()


	def run(self):
		while True:
			try:
				if self.active:
					time.sleep(self.interval / 1000)
					pygame.event.post(self.event)
			except Exception as ex:
				print(ex)
				break


	def stop(self):
		self.active = False

class TargetTimer(Timer):
	def __init__(self, timer_id, time_interval, target, timer_name=None):
		super().__init__(timer_name, time_interval, timer_name)
		self.target = target
		self.event.target = target

	def run(self):
		while True:
				if self.active:
					time.sleep(self.interval / 1000)
					pygame.event.post(self.event)
					self.target()
			except Exception as ex:
				print(ex)
				break

