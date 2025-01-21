import pygame


class Font:

	def __init__(self, name, font_name=None, size=16, antialias=True):
		self._name = name if name is None else f'Font{id(self)}'
		self._font = pygame.font.Font(font_name, size)
		self._antialias = antialias

	@staticmethod
	def get_default_font_attrs():
		return {
			'bold': False,
			'underline': False,
			'strikethrough': False,
			'italic': False,
			'direction': pygame.DIRECTION_LTR,
			'antialias': True
		}

	def __getattr__(self, key):
		return getattr(self._font, key)

	def get_antialias(self):
		return self._antialias

	def set_antialias(self, is_antialias):
		self._antialias = is_antialias

	def update_font_attrs(self, font_attrs):
		font_attrs = self.get_default_font_attrs()
		for key, attr in font_attrs.items():
			try:
				getattr(self, 'set_' + key)(font_attrs.get(key, attr))
			except AttributeError:
				continue

	def render(self, text, color, bg_color, rect=None):
		if rect:
			size = rect.w
		else:
			size = 0
		return self._font.render(text, self._antialias, color, bg_color, size)


