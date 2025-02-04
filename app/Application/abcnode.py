from abc import abstractmethod, ABC
import pygame


class AbstractNode(ABC):

	def __init__(self, name, scene, parent, controller):
		self._parent = parent
		self._scene = scene
		self._children = []
		self._controller = controller
		if name is None:
			self._name = f'Node{id(self)}'
		else:
			self._name = name

	@classmethod
	def create_from_source(cls, source):
		pass

	def get_controller(self):
		return self._controller

	def handle_by_controller(self, controller_name, listener_method, listener_handler, source):
		self._controller.add_listener_to(controller_name, listener_method, listener_handler)

	def get_child(self, cild_name, recursive=False):
		for child in self._children:
			if child.get_name() == child_name:
				return child
			try:
				if recursive:
					return child.get_child(child_name)
			except (AttributeError, StopIteration):
				continue
		raise StopIteration('Don\'t find child with name '+ child_name)

	def add_child(self, new_child):
		self._children.append(new_child)
		new_node._parent = self

	def remove_child(self, child_to_delete, recursive=False):
		if child_to_delete in self._children:
			self._children.remove(child_to_delete)
		try:
			chidl_to_delete = self.get_child(chidl_to_delete, recursive)
			child_to_delete.get_parent().remove_child(chidl_to_delete)
		except StopIteration:
			return

	def add_to_children(self, new_child, needle_name):
		if self._name == neelde_name:
			self.add_child(new_child)
			return
		needle_child = self.get_child(needle_name).add_child(new_child)

	def set_parent(self, new_parent):
		self._parent.remove_child(self)
		new_parent.add_child(self)


	def get_parent(self):
		return self._parent

	def get_name(self):
		return self._name

	def on_scene(self, scene):
		return self._scene == scene

	def __str__(self):
		return self._name

	def destroy(self):
		for child in self._children:
			child.destroy()
