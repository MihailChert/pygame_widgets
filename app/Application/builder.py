import warnings
import os.path as path
import json
from .source import Source


class Builder:

	def __init__(self, sources):
		self._sources = sources

	@classmethod
	def build_from(cls, build_content):
		if isinstance(build_content, dict):
			sources = cls.build_from_dict(build_content)
			return cls(sources)
		if isinstance(build_content, list):
			source = cls.build_from_list(build_content)
			return cls(source)
		if isinstance(build_content, str) and path.isfile(build_content) and build_content[-4:] == 'json':
			return cls.build_from_json(build_content)

	@classmethod
	def build_from_json(cls, content):
		with open(content) as file_cont:
			content = json.load(file_cont)
		if isinstance(content, dict):
			return cls(cls.build_from_dict(content))
		elif isinstance(content, list):
			return cls(cls.build_from_list(content))

	@staticmethod
	def build_from_dict(content):
		sources = []
		for source_type, type_content_list in content.items():
			for type_content in type_content_list:
				type_content['type'] = source_type
				source = Source.build_from_dict(type_content)
				sources.append(source)
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
	def load(queue, controller):
		queue.reverse()
		for source in queue:
			source.load(controller)

	@staticmethod
	def tree_to_queue(tree):
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
		if isinstance(needle_name, Source):
			return needle_name
		elif isinstance(needle_name, str):
			for source in haystack:
				if source.get_name() == needle_name:
					return source
			raise NameError(f'Invalid source name {needle_name} for current scene.')
		raise TypeError('Unsupported type for source name.')

	def link_sources(self):
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
		root = self._sources[0]
		while bool(root.depended):
			if id(root) == id(root.depended):
				raise RuntimeError(f'Two or more node have same name: {root.get_name()}.')  # TODO: change error type
			root = root.depended
		self._sources = [root]

	@staticmethod
	def source_to_weak_tree(tree):
		res = {}
		for element in tree:
			res = {
				'name': element.get_name(),
				'dependencies': Builder.source_to_weak_tree(element.get_dependencies())
			}
		return res

	def build_sources(self, controller):
		self.link_sources()
		root = self._sources[0]
		while root.depended is not None:
			root = root.depended
		self.load(self.tree_to_queue([root]), controller)
		return root.get_content()
