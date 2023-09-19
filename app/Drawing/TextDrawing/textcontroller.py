import pygame
from ...Application import AbstractController


class TextController(AbstractController):

    def __init__(self, name, app):
        super().__init__(name, app)
        self._event_id = self.create_event_id()

    @classmethod
    def get_settings_loader(cls, source):
        app = source.meta['application']
        app.update_option('custom_fonts', source.check_meta('fonts', default={}))
        return super(cls, TextController).get_settings_loader(source)

    def init(self, app):
        self._app = app
        pygame.font.init()
        self.logger.info('init text')

    def after_init(self):
        pass

    def has_event_type(self, event_type):
        return event_type == self._event_id or event_type == self._name

    def get_font(self, font_name=None, font_size=16):
        if self._app.is_option_exist('custom_font') and font_name in self._app.get_option('custom_fonts').keys():
            font_name = self._app.is_option_exist('custom_font')[font_name]
        return pygame.font.Font(font_name, font_size)

    def destroy(self, event):
        pygame.font.quit()

    def get_text_loader(self, source):
        source.meta['controller'] = self
        cls = None
        for dependence in source.get_dependencies():
            if dependence.get_name() == source.get_source():
                cls = dependence.get_content()
                break
        return cls.create_from_source(source)

    def get_font_loader(self, source):
        self.logger.info('get font loader')
        pass
