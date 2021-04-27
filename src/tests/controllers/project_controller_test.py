from pathlib import Path
from pyfakefs import fake_filesystem_unittest

from controllers.project_controller import project_controller
from config.config import config
from db.db_connection import database
from utils.filesystem import file_system
from utils.exceptions import ProjectExistsError

class ProjectControllerTest(fake_filesystem_unittest.TestCase):
    #
    #   Setup
    #

    @classmethod
    def setUpClass(cls):
        config.open_config()

    def setUp(self):
        database.connect(':memory:')
        self.setUpPyfakefs()

    def tearDown(self):
        database.close()

    #
    #   Tests
    #

    def test_create_succeeds(self):
        project_controller.create_project('test_project', '.')

    def test_create_fails_with_existing_project(self):
        project_controller.create_project('test_project', '.')

        self.assertRaises(ProjectExistsError,
            project_controller.create_project, 'test_project', '.')

    def test_get_projects_returns_all_names(self):
        project_controller.create_project('test_project_1', '.')
        project_controller.create_project('test_project_2', '.')
        project_controller.create_project('test_project_3', '.')

        self.assertEqual(len(project_controller.get_projects()), 3)

    def test_get_project_by_id_returns_correct_project(self):
        project_controller.create_project('test_project_1', '.')
        project_controller.create_project('test_project_2', '.')
        project_controller.create_project('test_project_3', '.')

        database.execute("""select project_id from Projects
                            where name = 'test_project_1'""")
        project_id = database.fetch_one()[0]

        self.assertEqual(project_id,
            project_controller.get_project_by_id(project_id).project_id)

