import pygame
from app import Node


class NodeAxisContainer(Node):

	def __init__(self, name, pos, size, parent, controller, bg_color):
		super().__init__(name, pos, size, parent, controller, bg_color)
		self.current_selected = 1
		self.selected = None

	def handle_by_controller(self, controller_name, listener_method, handler, source):
		if order := source.check_meta('listeners_order', default={})[controller_name][listener_method]:
			self.get_controller().add_listener_to(controller_name, listener_method, handler, order=order)
		else:
			self.get_controller().add_listener_to(controller_name, listener_method, handler)

	def move_left(self, event):
		if event.type == pygame.KEYUP:
			return
		leave = self.find(f'axis{self.current_selected}')
		self.current_selected = self.clamp(self.current_selected-1, 1, 3)
		selected = self.find(f'axis{self.current_selected}')
		self.get_controller().create_event('move_left', leave=leave, selected=selected)

	def move_right(self, event):
		if event.type == pygame.KEYUP:
			return
		leave = self.find(f'axis{self.current_selected}')
		self.current_selected = self.clamp(self.current_selected+1, 1, 3)
		selected = self.find(f'axis{self.current_selected}')
		self.get_controller().create_event('move_right', leave=leave, selected=selected)

	def select(self, event):
		if event.type == pygame.KEYUP:
			return
		if self.selected is None:
			self.selected = self.find(f'axis{self.current_selected}')
			selected = self.selected
			self.get_controller().create_event('select', selected=selected)
			return
		selected_from = self.selected
		selected_to = self.find(f'axis{self.current_selected}')
		self.get_controller().create_event('select', selected_from=selected_from, selected_to=selected_to)
		self.selected = None

	@staticmethod
	def clamp(value, min_val, max_val):
		if value > max_val:
			return max_val
		if value < min_val:
			return min_val
		return value
