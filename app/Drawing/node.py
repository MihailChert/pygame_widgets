from .abcnode import AbstractNode
import pygame


class Node(AbstractNode):

	def __init__(self, name, pos, size, parent, bg_color=(0, 0, 0)):
		super().__init__(name, pos, size, parent)
		self._children = []
		self.background_color = pygame.Color(bg_color)
		self._has_change = True

	@classmethod
	def create_from_source(cls, source):
		node = cls(source.get_name(), source.meta['pos'], source.meta['size'], None, source.meta['background'])
		for dependence in source.get_dependencies():
			if dependence.get_type() != source.TYPE.code:
				dependence.get_content()._parent = node
				node.add_child(dependence.get_content())
		controller = source.meta['controller']
		for controller_name, listeners in source.meta.get('listeners', {}).items():
			for listener_method, listener_handler in listeners.items():
				controller.add_listener_to(controller_name, listener_method, getattr(node, listener_handler))
		return node

	def add_child(self, new_node):
		self._children.append(new_node)
		self.union_rect(new_node.get_rect())

	def union_rect(self, union_rect):
		union_rect = self.convert_rect_to_global(union_rect)
		self._rect = self._rect.union(union_rect)
		if self._parent is not None:
			self._parent.union_rect(self._rect)

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

	def update(self, controller):  # TODO: try make like decorator
		self._has_change = True
		rect = pygame.Rect((0, 0), controller.factory.get_surface().get_size())
		controller.calc_update_zone(self.convert_rect_to_global(rect))

	def _draw(self, factory, controller):
		if self._parent is None:
			factory.draw_simple_figure().draw_background(self.background_color)
		else:
			rect = self.get_global_rect()
			factory.draw_simple_figure().rect(self.background_color, rect)
		self.draw(factory)
		for child in self._children:
			if isinstance(child, pygame.Surface):  # TODO: draw image or text
				pass
			child._draw(factory, controller)
		self._has_change = False

	def draw(self, factory):
		pass

	def destroy(self):
		for child in self._children:
			child.destroy()
