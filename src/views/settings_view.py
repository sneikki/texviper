from PySide2.QtCore import QObject, Slot

from views.view import View
from config.config import config


class SettingsView(View):
    def __init__(self, engine):
        super().__init__(engine)

        self.load_settings()

    def load_settings(self):
        """ Creates entries for each key-value pair in configuration.
        """
        self.load_setting('dbPath', 'text', config.get_value('db_path'))
        self.load_setting('dbName', 'text', config.get_value('db_name'))
        self.load_setting('projectLocation', 'text',
                          config.get_value('default_project_path'))
        self.load_setting('templateLocation', 'text',
                          config.get_value('default_template_path'))
        self.load_setting('rootFilename', 'text',
                          config.get_value('root_filename'))
        self.load_setting('accentColor', 'text',
                          config.get_value('accent_color'))
        self.load_setting('editorFont', 'text',
                          config.get_value('editor_font'))

    def load_setting(self, setting_name, prop, value):
        """ Creates entry for a single key-value pair.
        """
        setting = self.root.findChild(QObject, setting_name)
        setting.setProperty(prop, value)

    def get_setting(self, setting_name, prop):
        """ Gets the value of a setting field from ui

            Returns:
                string: value of the field
        """
        setting = self.root.findChild(QObject, setting_name)
        return setting.property(prop)

    @Slot()
    def save_settings(self):
        """ Called when save button is clicked. Writes the config values
            to the configuration file.
        """
        config.set_value('db_path', self.get_setting('dbPath', 'text'))
        config.set_value('db_name', self.get_setting('dbName', 'text'))
        config.set_value('default_project_path',
                         self.get_setting('projectLocation', 'text'))
        config.set_value('default_template_path',
                         self.get_setting('templateLocation', 'text'))
        config.set_value('root_filename', self.get_setting(
            'rootFilename', 'text'))
        config.set_value(
            'accent_color', self.get_setting('accentColor', 'text'))
        config.set_value('editor_font', self.get_setting('editorFont', 'text'))

        config.save_config()
