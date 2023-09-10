from app import Node


class NodeMainBar(Node):

	def draw(self, factory):
		factory.draw_simple_figure().rect(self.background_color, self.get_global_rect())
