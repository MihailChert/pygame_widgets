import pygame
from ...Application import AbstractPhysicalNode
from .font import Font


class SimpleText(AbstractPhysicalNode):

	def __init__(self, name, pos, size, scene, parent, controller, font, text, color, bg_color=None):
		super().__init__(name, pos, size, scene, parent, controller)
		self.font = font
		self._text = text
		self.color = color
		self.bg_color = bg_color
		self._parent = parent
		self._rendered_text = None
		self.render()
		self._rect.size = self._rendered_text.get_size()

	@classmethod
	def create_from_source(cls, source):
		font = source.meta.get('font', None)
		font = Font(source.get_name()+'Font', source.meta.get('font_name', None), source.meta.get('font_size', 16))
		font.update_font_attrs(source.meta)
		bg_c = None if source.meta.get('bg_color', True) else pygame.Color(source.meta['bg_color'])
		return cls(
			source.get_name(),
			source.check_meta('pos', True),
			source.check_meta('size', default=(0, 0)),
			source.get_root().get_name(),
			None,
			source.meta['controller'],
			font,
			source.check_meta('text', True),
			source.check_meta('color', True),
			bg_c
		)

	def get_name(self):
		return self._name

	def update(self, font=None, font_dict=None, text=None):
		font = self.font if font is None else font
		if font_dict is not None:
			self.font.update_font_attrs(font_dict)
		text = self._text if text is None else text
		self.font = font
		self._text = text
		del self._rendered_text
		self._rendered_text = None
		self.render()

	def render(self):
		if self._rendered_text is None:
			if self._parent is not None:
				size = self._rect if not self._rect else self._parent.get_local_rect()
			else:
				size = self.get_local_rect()
			self._rendered_text = self.font.render(self._text, self.color, self.bg_color, size)

	def _draw(self):
		self.render()
		self._controller.get_app().get_screen().blit(self._rendered_text, self.get_global_rect())

	def destroy(self):
		try:
			del self._rendered_text
		except AttributeError:
			pass
