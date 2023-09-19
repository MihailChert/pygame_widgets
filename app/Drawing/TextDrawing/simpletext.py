import pygame


class SimpleText:

	def __init__(self, name, font, text, antialias, color, parent, bg_color=None):
		self._name = name
		self.font = font
		self._text = text
		self.color = color
		self.antialias = antialias
		self.bg_color = bg_color
		self._parent = parent
		self._rendered_text = None

	@classmethod
	def create_from_source(cls, source):
		font = source.meta.get('font', None)
		if font is None:
			font = pygame.font.Font(source.meta.get('font_name', None), source.meta.get('font_size', 16))
		else:
			font = pygame.font.Font(*font)
		cls.set_font_attrs_from_dict(font, source.meta)
		bg_c = None if source.meta.get('bg_color', True) else pygame.Color(source.meta['bg_color'])
		return cls(
			source.get_name(),
			font,
			source.meta['text'],
			bool(source.meta.get('antialias', False)),
			source.meta['color'],
			source.depended,
			bg_c
		)

	@staticmethod
	def set_font_attrs_from_dict(font, font_attrs_dict):
		SimpleText.try_set_font_attr(font, font_attrs_dict, 'bold')
		SimpleText.try_set_font_attr(font, font_attrs_dict, 'underline')
		SimpleText.try_set_font_attr(font, font_attrs_dict, 'strikethrough')
		SimpleText.try_set_font_attr(font, font_attrs_dict, 'italic')
		SimpleText.try_set_font_attr(font, font_attrs_dict, 'direction', pygame.DIRECTION_LTR)

	@staticmethod
	def get_font_attrs(font):
		return {
			'bold': font.get_bold(),
			'underline': font.get_underline(),
			'strikethrough': font.get_strikethrough(),
			'italic': font.get_italic(),
			'direction': font.direction
		}

	@staticmethod
	def try_set_font_attr(font, font_dict, font_attr, default=False):
		try:
			getattr(font, 'set_' + font_attr)(font_dict.get(font_attr, default).lower != str(default).lower())
		except AttributeError:
			getattr(font, 'set_' + font_attr)(font_dict.get(font_attr, default) != default)

	def get_name(self):
		return self._name

	def get_rect(self):
		return pygame.Rect(0, 0, 0, 0)

	def update(self, font=None, font_dict=None, text=None):
		font = self.font if font is None else font
		if font_dict is not None:
			self.set_font_attrs_from_dict(font, font_dict)
		text = self._text if text is None else text
		self.font = font
		self._text = text
		del self._rendered_text
		self._rendered_text = None
		self.render()

	def render(self):
		if self._rendered_text is None:
			size = self._parent.get_rect().size
			self._rendered_text = self.font.render(self._text, self.antialias, self.color, self.bg_color, size[0])

	def _draw(self, controller):
		self.render()
		controller._app.get_screen().blit(self._rendered_text, self._parent.get_global_rect())

	def destroy(self):
		try:
			del self._rendered_text
		except AttributeError:
			pass