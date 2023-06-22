from enum import Enum


class Source:

	def __init__(self, content_type, source_name, source, meta=None):
		self._type = content_type
		self._name = source_name
		self._source = source
		self.meta = meta
		self._content = None

	def get_type(self):
		return self._type

	def get_source(self):
		return self._source

	def get_name(self):
		return self._name

	def get_content(self):
		return self._content

	def is_load(self):
		return self._content is not None

	def set_content(self, content):
		self._content = content

	def get_loader_method(self):
		return f'get_{self._type.name}_loader'

	def load(self, controller):
		content = controller.find_loader(self)(self)
		if content is not None and not isinstance(content, (int, str, tuple, bool)):
			self._content = content


class SourceType(Enum):

	image = 'img'
	sound = 'sound'
	node = 'node'
	text = 'text'
	settings = 'config'
	save = 'save'
