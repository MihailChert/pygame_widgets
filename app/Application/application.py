from .appfactory import AppFactory
'''
All action before create window and start controllers listeners
Import controllers and factories from config
'''


class Application:

	INCLUDE_FACTORY = {}

	def __init__(self, factories=dict(), config=dict()):
		self.factories_config = self._update_config(self.get_default_factories(), factories)
		self.config = self.get_default_config()
		self.config.update(config)
		self._main_factory = self.factories_config['main']('main', self, self.factories_config)

	@staticmethod
	def get_default_factories():
		return {'main': AppFactory}

	@staticmethod
	def get_default_config():
		return {
			'main': {
				'display_mod': (500, 500),
				'display_flag': 0,
				'caption': 'Game'
			}
		}

	@staticmethod
	def _update_config(global_config, custom_config):
		for conf_fact_name in global_config.keys():
			if conf_fact_name in custom_config.keys():
				global_config[conf_fact_name].update(custom_config[conf_fact_name])
		for conf_fact_name, fact_conf in custom_config.items():
			if conf_fact_name not in global_config.keys():
				global_config[conf_fact_name] = fact_conf
		return global_config

	def update_includes(self, factory_name, factory):
		self.factories_config[factory_name] = factory
		if 'main' == factory_name:
			self._main_factory = factory
		else:
			self._main_factory.update_factory(factory_name, factory)

	def run(self):
		self._main_factory.init()
		clock = self._main_factory.get_clock()
		controllers = self._main_factory.get_all_controllers()
		while True:
			clock.tick()
			for controller in controllers:
				controller._listen()
