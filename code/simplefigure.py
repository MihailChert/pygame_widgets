import pygame
from app import Node


class NodeSimpleFigure(Node):

	@classmethod
	def create_from_source(cls, source):
		node = super(cls, NodeSimpleFigure).create_from_source(source)
		node.figure = source.check_meta('figure', default='rect')
		return node

	def draw(self, factory):
		getattr(factory.draw_simple_figure(), self.figure)(self.background_color, self.get_global_rect())
