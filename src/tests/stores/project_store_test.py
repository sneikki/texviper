from pathlib import Path
from uuid import uuid4 as uuid
import json
from pyfakefs import fake_filesystem_unittest

from stores.project_store import (
    project_store, CreateProjectError
)
from models.project import Project

# todo: move initialization to setUp


class ProjectStoreTest(fake_filesystem_unittest.TestCase):
    def setUp(self):
        self.setUpPyfakefs()

    def test_create_project(self):
        project = Project('test_project', '.')
        project_store.create_project(project)

        self.assertTrue(Path('test_project').exists())

    def test_create_project_fails_with_existing_directory(self):
        project = Project('existing_project', '.')
        project_store.create_project(project)

        self.assertRaises(CreateProjectError,
                          project_store.create_project, project)

    def test_create_project_does_not_create_config_to_existing_directory(self):
        Path('test_project').mkdir()

        project = Project('test_project', '.')

        try:
            project_store.create_project(project)
        except CreateProjectError:
            pass

        self.assertFalse(Path('test_project/projectrc.json').exists())

    def test_create_project_fails_without_permission(self):
        Path('000_dir').mkdir(0o000)

        project = Project('project', '000_dir')
        self.assertRaises(CreateProjectError,
                          project_store.create_project, project)

    def test_create_project_initializes_project(self):
        project = Project('test_project', '.')
        project_store.create_project(project)

        self.assertTrue(Path('test_project/projectrc.json').exists())

    def test_init_project_initializes_with_correct_values(self):
        project_id = str(uuid())
        name = 'test_project'
        path = '.'

        project = Project(name, path, project_id)
        project_store.create_project(project)

        rc_config = json.loads(Path('test_project/projectrc.json').read_text())
        self.assertEqual(rc_config['id'], project_id)
        self.assertEqual(rc_config['name'], name)
