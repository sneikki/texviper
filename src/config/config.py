from json import dumps, load
from pathlib import Path
from shutil import copyfile

from utils.literal import literals

CONFIG_PATH = '~/.texviper/config.json'

class Config:
    def __init__(self):
        self.config_values = dict()

    def create_project_config(self, project_id, name):
        project_config = dict()

        project_config['name'] = name
        project_config['project_id'] = project_id

        return dumps(project_config)

    def get_value(self, name):
        return self.config_values[name]

    def set_value(self, name, value):
        pass

    def open_config(self, cfg_path=None):
        path = Path(cfg_path or CONFIG_PATH).expanduser()

        try:
            if not path.exists():
                # Copy config file to config path
                copyfile('src/config/default_config.json', path)

            with open(path) as config_file:
                self.config_values = load(config_file)
        except PermissionError:
            # Cannot create config file, use default config

            with open('src/config/default_config.json') as config_file:
                self.config_values = load(config_file)

config = Config()
