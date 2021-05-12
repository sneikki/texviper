from pathlib import Path
from uuid import uuid4 as uuid
from pyfakefs import fake_filesystem_unittest

from stores.template_store import template_store
from models.template import Template
from config.config import config
from db.db_connection import database
from utils.filesystem import file_system

class TemplateStoreTest(fake_filesystem_unittest.TestCase):
    #
    #   Setup
    #

    @classmethod
    def setUpClass(cls):
        config.open_config(use_default=True)

    def setUp(self):
        database.connect(':memory:')
        self.setUpPyfakefs()

    def tearDown(self):
        database.close()

    def test_create_creates_file(self):
        template = Template('test_template', 'test_template.tex', '~/.texviper/templates')
        template_store.create(template, '')

        self.assertTrue(
            Path('~/.texviper/templates/test_template.tex').expanduser().exists()
        )

    def test_create_inserts_to_database(self):
        template = Template('test_template', 'test_template.tex', '~/.texviper/templates')
        template_store.create(template, '')

        database.execute(
            '''select * from Templates where name="test_template"'''
        )
        result = database.fetch_one()

        self.assertEqual(len(result), 4)

    def test_delete_removes_file(self):
        template = Template('test_template', 'test_template.tex', '~/.texviper/templates')
        template_store.create(template, '')

        template_store.delete_one(template.template_id)
        self.assertFalse(file_system.file_exists(
            Path('~/.texviper/templates/test_template.tex').expanduser()
        ))
