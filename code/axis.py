import pygame
from app import Node
from code.simplefigure import NodeSimpleFigure


class NodeAxis(Node):

	def __init__(self, name, pos, size, parent, controller, bg_color=(0, 0, 0)):
		super().__init__(name, pos, size, parent, controller, bg_color)
		self._max_width = 66
		self._min_width = 10
		self.selected = False
		self.hover = False

	def start_game(self, event):
		width_step = (self._max_width - self._min_width) // 5
		start_pos = 5
		height = (self.get_rect().h - 5) // 5
		for node_width in range(1, 6):
			segment = NodeSimpleFigure(
				f'segment{node_width}',
				(self._max_width - node_width*width_step - 10, start_pos),
				(node_width*width_step*2 + 50, height),
				self,
				self.get_controller(),
				pygame.Color(node_width*30, 30, 30, 0)
			)
			segment.figure = 'rect'
			self.add_child(segment)
			start_pos += height

	def select(self, event):
		if event.type == pygame.KEYUP:
			return
		try:
			if self is event.selected:
				self.change_color()
		except AttributeError:
			pass
		try:
			if self is event.selected_from:
				if event.selected_from is not event.selected_to:
					self.move(event.selected_to)
				self.change_color()
		except AttributeError:
			pass

	def get_min_segment(self):
		min_segment = None
		i = 1
		while min_segment is None and i < 6:
			try:
				min_segment = self.find(f'segment{i}')
			except StopIteration:
				i += 1
		return min_segment

	def move(self, select_to):
		min_segment_from = self.get_min_segment()
		if min_segment_from is None:
			return
		min_segment_to = select_to.get_min_segment()
		if min_segment_to is not None and min_segment_to.get_name()[-1] < min_segment_from.get_name()[-1]:
			return
		self.get_controller().calc_update_zone(min_segment_from.get_global_rect())
		select_to.add_segment(min_segment_from)
		self._children.remove(min_segment_from)

	def add_segment(self, segment):
		min_segment = self.get_min_segment()
		start_y = self.get_rect().height
		if min_segment is not None:
			start_y = min_segment.get_rect().y
		segment_rect = segment.get_rect()
		segment_rect.y = start_y - segment_rect.h
		self.add_child(segment)
		self.get_controller().calc_update_zone(segment.get_global_rect())

	def change_color(self):
		self.selected = not self.selected
		column = self.find('axisColumn' + self.get_name()[-1])
		if self.selected:
			column.background_color = pygame.Color(200, 0, 200, 255)
		else:
			column.background_color = pygame.Color(0, 255, 0, 255)
		self.get_controller().calc_update_zone(column.get_global_rect())

	def move_left(self, event):
		try:
			column = self.find('axisColumn' + self.get_name()[-1])
			if event.selected is self and not self.selected:
				column.background_color = pygame.Color(255, 0, 0, 255)
				self.get_controller().calc_update_zone(column.get_global_rect())
				return
			if event.leave is self and not self.selected:
				column.background_color = pygame.Color(0, 255, 0, 255)
			self.get_controller().calc_update_zone(column.get_global_rect())
		except AttributeError as er:
			self.get_controller().logger.error(er)

	def move_right(self, event):
		try:
			column = self.find('axisColumn' + self.get_name()[-1])
			if event.selected is self and not self.selected:
				column.background_color = pygame.Color(255, 0, 0, 255)
				self.get_controller().calc_update_zone(column.get_global_rect())
			if event.leave is self and not self.selected:
				column = self.find('axisColumn' + self.get_name()[-1])
				column.background_color = pygame.Color(0, 255, 0, 255)
			self.get_controller().calc_update_zone(column.get_global_rect())
		except AttributeError as er:
			self.get_controller().logger.error(er)
