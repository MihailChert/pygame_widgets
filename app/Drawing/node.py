from ..Application import AbstractPhysicalNode
import pygame


class Node(AbstractPhysicalNode):

	def __init__(self, name, pos, size, scene, parent, controller, bg_color):
		super().__init__(name, pos, size, scene, parent, controller)
		self.background_color = pygame.Color(bg_color)
		self._has_change = True

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

	def update(self, event):
		self._has_change = True
		rect = pygame.Rect((0, 0), self._controller._app.get_screen().get_size())
		self._controller.calc_update_zone(self.get_global_rect())

	def _get_surface(self):
		return None

	def get_surface(self):
		parent = self._parent
		surface = None
		while parent is not None:
			try:
				surface = self._get_surface()
			except AttributeError:
				continue
			if surface is not None:
				return surface
		return self._controller.get_app().get_screen()

	def _draw(self, surface=None):
		if surface is None:
			surface = self.get_surface()
		self.draw(surface)
		for child in self._children:
			try:
				child._draw(surface) # TODO: draw image or text
			except AttributeError:
				continue
		self._has_change = False

	def draw(self, surface=None):
		pass
