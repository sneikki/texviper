from json import dumps, dump, load
from pathlib import Path
from shutil import copyfile

from utils.literal import literals
from utils.filesystem import file_system

CONFIG_PATH = '~/.texviper'
CONFIG_NAME = 'config.json'

class Config:
    def __init__(self):
        self.config_values = dict()
        self.opened_successfully = False

    def create_project_config(self, project_id, name):
        project_config = dict()

        project_config['name'] = name
        project_config['project_id'] = project_id

        return dumps(project_config)

    def get_value(self, name):
        return self.config_values[name]

    def set_value(self, name, value):
        self.config_values[name] = value

    def open_config(self, cfg_path=None):
        path = Path(cfg_path or CONFIG_PATH).expanduser()

        try:
            if not path.exists():
                # Copy config file to config path
                file_system.create_directory(path)
                copyfile('src/config/default_config.json', path / CONFIG_NAME)

            with open(path / CONFIG_NAME) as config_file:
                self.config_values = load(config_file)

            self.opened_successfully = True
        except PermissionError:
            # Cannot create config file, use default config

            with open('src/config/default_config.json') as config_file:
                self.config_values = load(config_file)

    def save_config(self, cfg_path=None):
        if not self.opened_successfully:
            raise Exception('Unable to save settings: opened in read-only mode')

        path = Path(cfg_path or CONFIG_PATH).expanduser() / CONFIG_NAME

        with open(path, 'w') as config_file:
            dump(self.config_values, config_file)

config = Config()
