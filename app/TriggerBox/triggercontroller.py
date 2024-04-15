import traceback
import pygame
from ..Application import AbstractController
from .motioneventenum import KeyEvent, MouseEvent, JoyEvent
from .abctriggerbox import AbstractTriggerBox
import pdb


class TriggerController(AbstractController):

	def __init__(self, name, app):
		super().__init__(name, app)
		self._aliases_names = {}
		self._aliases_keys = {}
		self._trigger_boxes = []
		self._button_boxes = []
		self._app.get_logger(name).info('create controller')
		self._event_id = self.create_event_id()

	@classmethod
	def get_settings_loader(cls, source):
		app = source.meta['application']
		controller = super().get_settings_loader(source)
		for alias, key in source.check_meta('key_aliases', default={}).items():
			controller.add_alias_keys(alias, key)
		return controller

	def init(self, app):
		self._app = app
		self.logger.info('init trigger controller')

	def after_init(self):
		return

	def create_event(self, event_type, **event_attrs):
		if event_type in self._listeners_list.keys():
			event_attrs['method'] = event_type
			event_type = self._event_id
		elif self.get_event_id(event_type) is not None:
			event_type = self.get_event_id(event_type)
		else:
			self.logger.warn('Event method has no in listeners or move event')
		event = pygame.event.Event(event_type, **event_attrs)
		pygame.event.post(event)

	def add_alias_keys(self, alias, keys): #TODO: add event type from motion enum
		for key in keys:
			if not key.get('mode', None):
				raise ValueError('Unexpected mode for key aliase')
			try:
				key['mode'] = self.get_event_id(key['mode'])
			except (KeyError, ValueError) as ex:
				raise ValueError('Ivalid key mode: %s. Mode unexpected in KeyEvent, MouseEvent or JoyEvent' % key['mode'])
			motion_event = KeyEvent.union(MouseEvent, JoyEvent)
			key['mode'] = motion_event(key['mode'])
			key = key['mode'].validate_key(key)
			key['mode'] = key['mode'].value
			try:
				if not self._aliases_keys.get(key['mode'], False) and key['name']:
					self._aliases_keys[key['mode']] = dict()
			except KeyError:
				pass

			try:
				if key.get('name', False):
					self._aliases_keys[key['mode']][key['name']] = self._aliases_names[alias]
				else:
					self._aliases_keys[key['mode']] = self._aliases_names[alias]
			except KeyError:
				if key.get('name', False):
					print(alias, key)
					self._aliases_names[alias] = self._aliases_keys[key['mode']][key['name']] = list()
				else:
					self._aliases_names[alias] = self._aliases_keys[key['mode']] = list()
			except TypeError:
				raise Value
		self.logger.debug(self._aliases_keys)
		self.logger.debug(self._aliases_names)

	def add_trigger_boxes(self, trigger_box):
		if isinstance(trigger_box, AbstractTriggerBox):
			self._trigger_boxes.append(trigger_box)
		else:
			raise TypeError('Triggered object should implement abstract trigger')

	def add_button_boxes(self, button_box):
		if isinstance(button_box, AbstractTriggerBox):
			self._button_boxes.append(button_box)
		else:
			raise TypeError('Triggered object should implement abstract trigger')

	def get_event_id(self, event_id_name):
		if isinstance(event_id_name, int):
			if event_id_name == self._event_id:
				return self._event_id
			try:
				return KeyEvent.union(MouseEvent, JoyEvent)(event_id_name).value
			except ValueError:
				raise ValueError(f'Unknown event id. Available from: {self._event_id}, and motion events from {type(self._motion_events)}')
		elif isinstance(event_id_name, str):
			if event_id_name == self._name:
				return self._event_id
			try:
				return KeyEvent.union(MouseEvent, JoyEvent)[event_id_name].value
			except KeyError:
				raise KeyError(f'Unknown event name. Availabel from: {self._name} and motion events from KeyEvent, MouseEvent, JoyEvent')

	def has_event_type(self, event_type):
		try:
			return self.get_event_id(event_type) and True
		except (ValueError, KeyError):
			return False

	def get_trigger_loader(self, source):
		source.meta['controller'] = self
		cls = None
		# pdb.set_trace()
		source.meta['pos'] = source.meta.get('pos', (0, 0))
		if not len(source.meta['pos']):
			source.meta['pos'] = (0, 0)
		for dependence in source.get_dependencies():
			if dependence.get_name() == source.get_source():
				cls = dependence.get_content()
				break
		try:
			return cls.create_from_source(source)
		except AttributeError as er:
			self.logger.info(traceback.format_exc())
			self.logger.error(er)
			raise RuntimeError(f'Проверить ресурс и загружаемый класс, {cls.__name__}, {er}') #TODO: change error

	def add_listener(self, listener_method, handler, order=None):
		if listener_method == 'update':
			if order is None:
				self._listners_update.append(handler)
			else:
				self._listners_update.insert(order, handler)
			return
		if listener_method in self._aliases_names.keys():
			print(listener_method, handler)
			if order is None:
				self._aliases_names[listener_method].append(handler)
			else:
				self._aliases_names[listener_method].insert(order, handler)
			return
		try:
			_listener_method = self.get_event_id(listener_method)
			listener_method = _listener_method
		except(KeyError, ValueError):
			pass
		try:
			if order is None:
				self._listeners_list[listener_method].append(handler)
			else:
				self._listeners_list[listenre_method].insert(order, handler)
		except (KeyError):
			self._listeners_list[listener_method] = [handler]

	def destroy(self, event):
		self.logger.info('destroy controller')
		for trigger in self._trigger_boxes:
			trigger.destroy()
		for trigger in self._button_boxes:
			trigger.destroy()

	def _test_collide_boxes(self):
		unchecked_triggers = self._trigger_boxes
		while len(unchecked_triggers):
			box = unchecked_triggers.pop()
			collides = box.collide(unchecked_triggers)
			self.create_event('collide', collided=collides)

	def _listen(self):
		self._test_collide_boxes()
		for event in pygame.event.get(KeyEvent.values(self._event_id, MouseEvent, JoyEvent)):
			listeners = self._listeners_list.get(event.type, list())
			_listeners = []
			if event.type in self._aliases_keys:
				e_dict = event.__dict__
				try:
					if e_dict.get('buttons', False):
						_listeners = self._aliases_keys[event.type][None]
						for button in e_dict['buttons']:
							if button in self._aliases_keys[event.type]:
								_listeners = _listenres + self._aliases_keys[event.type][button]
					_listeners = self._aliases_keys[event.type][e_dict.get('key', e_dict.get('button', False))]
				except (KeyError, IndexError) as er:
					self.logger.warn(er)
					if isinstance(self._aliases_keys[event.type], dict):
						raise RuntimeError('Invalid key event alias %s, %s' % (pygame.event.event_name(event.type), str(event.__dict__)))
					
					_listeners = self._aliases_keys[event.type]


			listeners = listeners + _listeners

			for listener in listeners:
				if self._app.is_option_exist('current_scene')\
					and listener.__self__.on_scene(
						self._app.get_option('current_scene')
					):
					listener(event)

		for update_handler in self._listeners_update:
			if self._app.is_option_exist('current_scene')\
				and update_handler.__self__.on_scene(
					self._app.get_option('current_scene')
				):
				update_handler(self)
