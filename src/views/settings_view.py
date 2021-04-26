from PySide2.QtCore import QObject, Slot

from config.config import config

class SettingsView(QObject):
    def __init__(self, engine):
        super().__init__()

        self.engine = engine
        self.root = self.engine.rootObjects()[0]

        self.load_settings()

    def load_settings(self):
        self.load_setting('dbPath', 'text', config.get_value('db_path'))
        self.load_setting('dbName', 'text', config.get_value('db_name'))
        self.load_setting('accentColor', 'text', config.get_value('accent_color'))
        self.load_setting('editorFont', 'text', config.get_value('editor_font'))

    def load_setting(self, setting_name, property, value):
        setting = self.root.findChild(QObject, setting_name)
        setting.setProperty(property, value)

    @Slot()
    def save_settings(self):
        config.set_value('db_path', self.get_setting('dbPath', 'text'))
        config.set_value('db_name', self.get_setting('dbName', 'text'))
        config.set_value('accent_color', self.get_setting('accentColor', 'text'))
        config.set_value('editor_font', self.get_setting('editorFont', 'text'))

        config.save_config()

    def get_setting(self, setting_name, property):
        setting = self.root.findChild(QObject, setting_name)
        return setting.property(property)
