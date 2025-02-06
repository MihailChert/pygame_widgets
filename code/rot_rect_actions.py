from app.Drawing import Rect
import pygame

class RotRect(Rect):

	def left_rot(self, e):
		self.move(-50, 0)
		self.rotate(-10)

	def right_rot(self, e):
		self.move(50, 0)
		self.rotate(10)