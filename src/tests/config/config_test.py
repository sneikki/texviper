import os
from pathlib import Path
from pyfakefs import fake_filesystem_unittest

from config.config import config
from utils.filesystem import file_system

class ConfigTest(fake_filesystem_unittest.TestCase):
    def setUp(self):
        self.setUpPyfakefs()
        self.fs.add_real_directory('src/config')

    def test_config_is_created(self):
        config.open_config()

        self.assertTrue(file_system.file_exists(
            Path('~/.texviper/config.json').expanduser()
        ))

    def test_config_contains_data(self):
        config.open_config()

        default_config = config.open_default_config()
        for prop in default_config:
            self.assertTrue(prop in config.config_values)

    def test_missing_values_are_supplied(self):
        file_system.create_directory(Path('~/.texviper'))
        file_system.create_file(Path('~/.texviper/config.json'))
        file_system.write(Path('~/.texviper/config.json'), '{ "accent_color": "purple }"')

        config.open_config()
        self.assertTrue('editor_font' in config.config_values)

    def test_default_config_is_used_when_invalid(self):
        file_system.create_directory(Path('~/.texviper'))
        file_system.create_file(Path('~/.texviper/config.json'))
        file_system.write(Path('~/.texviper/config.json'), '{ "accent_color": "purple, }"')

        default_config = config.open_default_config()
        for prop in default_config:
            self.assertTrue(prop in config.config_values)
        
    def test_values_are_saved(self):
        config.open_config()
        config.set_value('accent_color', 'blue')
        config.save_config()
        config.config_values = None
        config.open_config()

        self.assertEqual(config.get_value('accent_color'), 'blue')
