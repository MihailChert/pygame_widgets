from app import Node


class NodeAxis(Node):

	def draw(self, factory):
		factory.draw_simple_figure().rect(self.background_color, self.get_global_rect())
