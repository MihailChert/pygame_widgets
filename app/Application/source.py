from enum import Enum


class SourceType(Enum):

	image = 'img'
	sound = 'sound'
	node = 'node'
	text = 'text'
	settings = 'config'
	save = 'save'
	scene = 'scene'


class Source:
	"""Класс Source хранит информацию о контенте который необходимо загрузить и зависимости этого ресурса от других ресурсов.
	Контентом могут быть быть любые типы указаные в перечислении SourceType.
	Является временым хранилищем для загруженого ресурса пока загружаются другие.

	Parameters
	----------
	_type: SourceType
		Хранит тип загружаемого контента.
		Определяет какой загрузщик будет использоватся для данного типа, который ищет контроллер.
	_name: str
		Имя загружаемого контента. Необходим для поиска по графу ресурсов в строителе.
	_source:
		Информация о том что загружать.
		Для загрузщика хранит информация:
		    о пути к ресурсу если это музыка, изображение, сохранения, конфигурации сцены, др информация хранящаяся на диске,
		    о имени класса, пути к классу или другому, если это узел или текст, или другая информация генерируема внутри программы
	meta: dict
		Хранит дополнительную информацию об загружаемом обекте.
		Информацию о дополнительной информации для каждого типа следует смотреть в документации загрузщеков или/и в загружаемом типе.
	_dependence: list[Source, str]
		Список ресурсов от которых зависит данный ресурс. Обычно много у узлов.
		Могут быть ссылки на другие ресурсы или имена других ресурсов.
	_content:
		Хранит загруженый ресурс. Хранение необходимо для загрузки других ресурсов загрузщикамию.
		Загружается только один раз.
	depended: Source
		Ссылка на ресурс, который зависит от текущего. Небходимо для нахождение корневого узла.
	"""

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
		"""Попытка преобразовать словарь в ресурс.

		Parameters
		----------
		content: dict
			Словарь должен иметь ключи описаные в параметрах класса без символа нижнего подчеркивания.
			Обязательные ключи:
				type == Source.type,
				name == Source.name,
				ref == Source.source,
				meta == Source.meta
			Не обязательные ключи:
				dependence == Source.dependence
		Returns
		-------
			Ресурс созданый в соответствии с переаным словарем
		"""
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
				content['type']
			,	content['name']
			,	content['ref']
			,	content['meta']
			,	dependence
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
		"""Замена ключ ресурса от которого зависит этот ресурс на ресуос.

		Parameters
		----------
		dependence: Source
			Найденый ресурс из графа ресурсов от которого зависит этот ресурс.
		d_index: int
			Если ресурс зависит от нескольких ресурсов, то необходимо указывать индекс заменяемого ресурса.
		"""
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
		"""Указание родительских ресурсов для поиска кореневого ресурса."""
		for dependence in self._dependence:
			dependence.depended = self

	def load(self, controller):
		"""Поиск загрузщика через контроллер и загрузка ресурса.
		Загрузк производится только один раз, если content не None.

		Parameters
		----------
		controller: AbstractController
		Контроллер который ищет загрузщик.
		"""
		content = controller.find_loader(self)(self)
		if content is not None and not isinstance(content, (int, str, tuple, bool)):
			self._content = content
