from pathlib import Path
from uuid import uuid4 as uuid
from json import loads
from datetime import datetime
from pyfakefs import fake_filesystem_unittest

from stores.project_store import project_store
from models.project import Project
from config.config import config
from db.db_connection import database
from utils.filesystem import file_system


class ProjectStoreTest(fake_filesystem_unittest.TestCase):
    #
    #   Setup
    #

    @classmethod
    def setUpClass(cls):
        config.open_config(use_default=True)

    def setUp(self):
        # IMPORTANT: initialization must be done in this order,
        # otherwise database tries to look for init_db.sql in
        # the fake file system
        database.connect(':memory:')
        self.setUpPyfakefs()

    def tearDown(self):
        database.close()

    #
    #   Tests
    #

    def test_create_initializes_resources(self):
        project = Project('test_project', '.')
        project_store.create(project)

        self.assertTrue(Path('test_project/projectrc.json').exists())

    def test_create_inserts_to_database(self):
        project = Project('test_project', '.')
        project_store.create(project)

        database.execute(
            """select * from Projects where name='test_project'""")
        res = database.fetch_one()

        self.assertEqual(len(res), 4)

    def test_create_inserts_correct_values_to_database(self):
        project_id = str(uuid())
        name = 'test_project'
        path = '.'
        timestamp = str(datetime.now())
        project = Project(name, path, project_id, timestamp)
        project_store.create(project)

        database.execute(
            """select * from Projects where name='test_project'""")
        res = database.fetch_one()
        print(res)
        self.assertEqual(res[0], project_id)
        self.assertEqual(res[1], name)
        self.assertEqual(res[2], path)
        self.assertEqual(res[3], timestamp)

    def test_create_fails_with_nonempty_path(self):
        file_system.create_directory(Path('test_project'))
        file_system.create_file(Path('test_project/file'))

        project = Project('test_project', '.')

        self.assertRaises(FileExistsError,
                          project_store.create, project)

        self.assertFalse(file_system.file_exists(
            Path('test_project/projectrc.json')))

    def test_create_fails_with_bad_permission(self):
        Path('permission_000').mkdir(0o000)

        project = Project('project', 'permission_000')
        self.assertRaises(PermissionError,
                          project_store.create, project)

    def test_create_initializes_project_correctly(self):
        project_id = str(uuid())
        name = 'test_project'
        path = '.'

        project = Project(name, path, project_id)
        project_store.create(project)

        conf = loads(Path('test_project/projectrc.json').read_text())
        self.assertEqual(conf['project_id'], project_id)
        self.assertEqual(conf['name'], name)

    def test_delete_removes_database_record(self):
        project = Project('test_project', '.')
        project_store.create(project)

        project_store.delete_one(project.project_id)
        database.execute(
            f"""select * from Projects where project_id='{project.project_id}'""")
        self.assertIsNone(database.fetch_one())

    def test_delete_removes_project_directory(self):
        project = Project('test_project', '.')
        project_store.create(project)

        project_store.delete_one(project.project_id)
        self.assertFalse(file_system.directory_exists(Path('test_project')))

    def test_deleting_nonexising_does_not_raise_error(self):
        project_store.delete_one("94039403")
