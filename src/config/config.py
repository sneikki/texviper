import os
from json import dumps, dump, load, JSONDecodeError
from pathlib import Path
from shutil import copyfile
from dotenv import load_dotenv

from utils.filesystem import file_system

try:
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))
except FileNotFoundError:
    pass

CONFIG_PATH = os.getenv('CONFIG_PATH')
CONFIG_NAME = os.getenv('CONFIG_NAME')

class Config:
    def __init__(self):
        self.config_values = dict()
        self.opened_successfully = False

    def create_project_config(self, project_id, name):
        """ Creates a dictionary representing project configuration

            Args:
                project_id (string): Project id to be insterted into config
                name (string): Project name to be inserted into config
        
            Returns:
                dict: Dictionary representing the project configuration
        """

        project_config = dict()

        project_config['name'] = name
        project_config['project_id'] = project_id

        return dumps(project_config)

    def get_value(self, name):
        """ Returns a single value from configuration

            Args:
                name (string): Name of the property to query

            Returns:
                any: Value from the configuration
        """
        return self.config_values[name]

    def set_value(self, name, value):
        """ Sets a single value to configuration

            Args:
                name (string): Name of the property to set
                value (any): Value of the property
        """
        self.config_values[name] = value

    def open_default_config(self):
        """ Opens the default configuration

            Returns:
                dict: Dictionary representing the default
                        configuration
        """
        with open('src/config/default_config.json') as default_config:
            return load(default_config)

    def open_config(self, cfg_path=None, use_default=False):
        """ Opens a custom configuration from path

        Args:
            cfg_path (str, optional): Custom path. Defaults to None.
            use_default (bool, optional): Use default configuration. Defaults to False.
        """
        if use_default:
            self.config_values = self.open_default_config()
            return

        path = Path(cfg_path or CONFIG_PATH).expanduser()

        try:
            if not (path / CONFIG_NAME).exists():
                # Copy config file to config path
                file_system.create_directory(path)
                copyfile('src/config/default_config.json', path / CONFIG_NAME)

            with open(path / CONFIG_NAME) as config_file:
                self.config_values = load(config_file)

            backup_config = self.open_default_config()

            for prop in backup_config:
                if not prop in self.config_values:
                    self.config_values[prop] = backup_config[prop]

            self.opened_successfully = True
        except (PermissionError, JSONDecodeError):
            # Cannot create config file, use default config
            self.config_values = self.open_default_config()

    def save_config(self, cfg_path=None):
        """ Save configuration

        Args:
            cfg_path (str, optional): Path to save the config. Defaults to None.
        """
        if not self.opened_successfully:
            return

        path = Path(cfg_path or CONFIG_PATH).expanduser() / CONFIG_NAME

        with open(path, 'w') as config_file:
            dump(self.config_values, config_file)


config = Config()
