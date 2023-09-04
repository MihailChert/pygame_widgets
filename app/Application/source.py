from enum import Enum


class SourceType(Enum):

	image = 'img'
	sound = 'sound'
	node = 'node'
	text = 'text'
	settings = 'config'
	code = 'class'
	save = 'save'
	file = 'file'

	config_image = {'unique': True, 'recursive': False}
	config_sound = {'unique': True, 'recursive': False}
	config_node = {'unique': False, 'recursive': False}
	config_text = {'unique': True, 'recursive': False}
	config_settings = {'unique': True, 'recursive': False}
	config_code = {'unique': True, 'recursive': False}
	config_factory = {'unique': True, 'recursive': False}
	config_save = {'unique': False, 'recursive': False}
	config_file = {'unique': False, 'recursive': True}

	def config(self):
		return getattr(self.__class__, 'config_' + self.name)

	def is_unique(self):
		return getattr(self.__class__, 'config_' + self.name)['unique']


class Source:

	TYPE = SourceType

	def __init__(self, content_type, source_name, source, meta=None, source_dependencies=None):
		self._type = content_type
		self._name = source_name
		self._source = source
		self.meta = meta
		self._dependence = source_dependencies
		self.depended = None
		self._content = None

	@classmethod
	def build_from_dict(cls, content):
		dependence = []
		if isinstance(content.get('dependence', None), dict):
			for source_name, source_data in content['dependence'].items():
				source_data['name'] = source_name
				source = cls.build_from_dict(source_data)
				dependence.append(source)
		elif isinstance(content.get('dependence', None), list):
			for source_data in content['dependence']:
				source = source_data
				if isinstance(source_data, dict):
					source = cls.build_from_dict(source_data)
				dependence.append(source)
		content['type'] = cls.TYPE(content['type'])
		return cls(
			content['type'],
			content['name'],
			content['ref'],
			content.get('meta', {}),
			dependence
		)

	def get_type(self):
		return self._type

	def get_source(self):
		return self._source

	def get_name(self):
		return self._name

	def get_content(self):
		return self._content

	def has_dependence(self):
		return self._dependence is not None and 0 != len(self._dependence)

	def get_dependencies(self):
		return self._dependence

	def update_dependencies(self, dependence, d_index=-1):
		if not isinstance(dependence, Source):
			raise TypeError('Dependence can be update only to Source type object.')
		if d_index != -1 and isinstance(self._dependence, list):
			self._dependence[d_index] = dependence
		else:
			self._dependence = dependence

	def is_load(self):
		return self._content is not None

	def set_content(self, content):
		self._content = content

	def get_loader_method(self):
		return f'get_{self._type.name}_loader'

	def propagate_depend(self):
		for dependence in self._dependence:
			dependence.depended = self

	def load(self, controller):
		if self.is_load():
			return
		content = controller.find_loader(self)(self)
		if content is not None and not isinstance(content, (int, str, tuple, bool)):
			self._content = content
