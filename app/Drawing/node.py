from .abcnode import AbstractNode
import pygame
import pdb


class Node(AbstractNode):

	def __init__(self, name, pos, size, scene, parent, controller, bg_color):
		super().__init__(name, pos, size, scene, parent)
		self._children = []
		self.background_color = pygame.Color(bg_color)
		self._has_change = True
		self._controller = controller

	@classmethod
	def create_from_source(cls, source):
		controller = source.meta['controller']
		try:
			scene = source.get_dependencies(0).get_content().get_scene()
		except (AttributeError, TypeError):
			scene = source.get_root().get_name()
		node = cls(
			source.get_name(),
			source.check_meta('pos', True),
			source.check_meta('size', True),
			scene,
			None,
			controller,
			source.check_meta('background', default=pygame.Color(0, 0, 0, 0))
		)
		for dependence in source.get_dependencies():
			if dependence.get_type() != source.TYPE.code:
				dependence.get_content()._parent = node
				node.add_child(dependence.get_content())
		for controller_name, listeners in source.check_meta('listeners', default={}).items():
			for listener_method, listener_handler in listeners.items():
				node.handle_by_controller(controller_name, listener_method, getattr(node, listener_handler), source)
		return node

	def handle_by_controller(self, controller_name, listener_method, listener_handler, source):
		self._controller.add_listener_to(controller_name, listener_method, listener_handler)

	def add_child(self, new_node):
		self._children.append(new_node)
		new_node._parent = self

	def get_controller(self):
		return self._controller

	def add_to_children(self, new_node, needle_node):
		if self._name == needle_node:
			self._children.append(new_node)
			self.union_rect(new_node.get_rect())
			return True
		for child in self._children:
			if child.add_to_chldren(new_node, needle_node):
				return True
		return False

	def find(self, needle):
		for child in self._children:
			if child.get_name() == needle:
				return child
			try:
				return child.find(needle)
			except (AttributeError, StopIteration):
				continue
		raise StopIteration('Don\'t find object')

	def update(self, event):
		self._has_change = True
		rect = pygame.Rect((0, 0), self._controller._app.get_screen().get_size())
		self._controller.calc_update_zone(self.convert_rect_to_global(rect))

	def _draw(self):
		self.draw()
		for child in self._children:
			if isinstance(child, pygame.Surface):  # TODO: draw image or text
				pass
			child._draw()
		self._has_change = False

	def draw(self):
		pass

	def __str__(self):
		return self._name

	def destroy(self):
		for child in self._children:
			child.destroy()
