import warnings
from .source import Source


class Builder:
	"""
	Строит из переданого графа дерева ресурсов.
	Дерево ресурсов строится в соответствии с зависимости ресурсов.
	После загружабтся данные ресурсов загрузщиками, которые вустраивают отношения внутри звгруженого обекта.

	Parameters
	----------
	sources: list
		Граф ресурсов
	"""

	def __init__(self, sources: list):
		self._sources = sources

	@classmethod
	def build_from(cls, build_content):
		"""
		Меотод автоматически определяющий тип из которого должно гененрироватся граф ресурсов
		Поддерживаемые типы: dict, list
		Parameters
		----------
		build_content
			Контент из которого должно генерировтся граф ресурсов

		Returns
		-------
		Загрузщик с гравом из ресурсов
		"""
		if isinstance(build_content, dict):
			sources = cls.build_from_dict(build_content)
			return cls(sources)
		if isinstance(build_content, list):
			source = cls.build_from_list(build_content)
			return cls(source)

	@staticmethod
	def build_from_dict(content):
		sources = []
		for source_name, source_data in content:
			source_data['name'] = source_name if source_data.get('name', None) is None else source_data['name']
			sources.append(Source.build_from_dict(source_data))
		return sources

	@staticmethod
	def build_from_list(content):
		sources = []
		count_match_name = {}
		for data in content:
			count_match_name[data['name']] = count_match_name.get(data['name'], 0) + 1
			if count_match_name[data['name']] > 1:
				warnings.warn(f'Unpredictable behavior for sources with dependence {data["name"]}')
				data['name'] = data['name'] + str(count_match_name[data['name']])
		for source_data in content:
			source = Source.build_from_dict(source_data)
			sources.append(source)
		return sources

	def add_source(self, new_source):
		if not len(self._sources) == 0 and self._sources[0].is_load():
			new_source.load()
			self._sources.append(new_source)
		elif not len(self._sources) or (not len(self._sources) == 0 and not self._sources[0].is_load()):
			self._sources.append(new_source)

	@staticmethod
	def load(queue: list, controller):
		"""
		Разворачивает очеред из дерева и вызывает загрузщики ресурсов.
		Развороточереди необходим для более раней загрузки ресурсов, которые не имеют зависемостей.
		Parameters
		----------
		queue: list
			Очередь созданая из дерева, в которой порядок элементов соответсвует обходу дерева в глубь(от корня к листьям)
		controller: AbstractController
			Контроллер в котором начинается поиск, если загрузщик не находится- ищет контролер приложения по всем контролерам.
		"""
		queue.reverse()
		for source in queue:
			source.load(controller)

	@staticmethod
	def tree_to_queue(tree):
		"""Обходит граф, одерщащий несвязные графы и деревья, вглубь и записывает посещеные ресурсы в очередь.
		Типы кроме ресурсов не попадают в очередь тк они могут быть именами для русерсов.
		Для увеличения скорости по обходу дерева при поиске и линковке ресурсов
		Parameters
		----------
		tree:
			Дерево или граф которые необходимо обойти один или более раз
		"""
		# TODO: Проверку на циклическую ссылку
		queue = tree.copy()
		result_queue = []
		while bool(queue):
			element = queue.pop(0)
			if not isinstance(element, Source):
				continue
			result_queue.append(element)
			if element.has_dependence():
				dependencies = element.get_dependencies()
				if isinstance(dependencies, list):
					queue.extend(dependencies)
				else:
					queue.append(dependencies)
		return result_queue

	@staticmethod
	def find(haystack, needle_name):
		"""
		Поиск ресурса в графе, конвертированого в очередь, по имени.
		Если в качестве имени передан ресурс, возвращается ресурс.
		Parameters
		----------
		haystack: list
			Граф конвертированый в очередь, для более быстрого поиска
		needle_name:
			Имя ресурсо который нужно найти в графе.

		Returns
		-------
		Ресерс с заданым именем

		Raises
		------
		NameError
			Если не найдено имя ресурса в очереди, обхода графа
		TypeError
			Если имя ресурса не строчка.
		"""
		if isinstance(needle_name, Source):
			return needle_name
		elif isinstance(needle_name, str):
			for source in haystack:
				if source.get_name() == needle_name:
					return source
			raise NameError(f'Invalid source name {needle_name} for current scene.')
		raise TypeError('Unsupported type for source name.')

	def link_sources(self):
		"""
		Связывает зависимости ресурсов из графа ресурсов в дерево ресурсов, для последующей загрузке.
		Заменяет идентификатор ресурса от которого зависит иследуемый ресурс на ресурс хранящийся в графе.
		"""
		# TODO: Проверка н ациклическую ссылку
		queue = self.tree_to_queue(self._sources)
		for source in queue:
			if source.has_dependence():
				depends = source.get_dependencies()
				try:
					for depend_ind, depend in enumerate(depends):
						source.update_dependencies(self.find(queue, depend), depend_ind)
				except TypeError:
					source.update_dependencies(self.find(queue, depends))
				source.propagate_depend()

	def build_sources(self, controller):
		"""
		Связывает и зергужает ресурсы.
		Parameters
		----------
		controller: AbstractController
			Контроллер в котором первоначально происхоит поиск загрузщика.
			Если загрузщик не найден, идет поиск по всем контролерам.

		Returns
		-------
		Контент корневого узла дерева, который зависет от остальных ресурсов и любой другой ресурс не зависит от текущего.
		"""
		self.link_sources()
		root = self._sources[0]
		while root.depended is not None:
			root = root.depended
		self.load(self.tree_to_queue([root]), controller)
		return root.get_content()
