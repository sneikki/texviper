from pathlib import Path
from pyfakefs import fake_filesystem_unittest

from controllers.project_controller import project_controller
from controllers.template_controller import template_controller
from config.config import config
from db.db_connection import database
from utils.exceptions import ProjectExistsError, InvalidValueError


class ProjectControllerTest(fake_filesystem_unittest.TestCase):
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

    #
    #   Tests
    #

    def test_create_succeeds(self):
        project_controller.create_project('test_project', '.')

    def test_project_is_initialized_correctly_with_template(self):
        template = template_controller.create_template('test template', 'test_template.tex', '~/.texviper/templates', 'test')
        project_controller.create_project('test_project', '~/.texviper/projects', template.name)

        self.assertEqual(
            Path('~/.texviper/projects/test_project/main.tex').expanduser().read_text(),
            'test'
        )

    def test_create_fails_with_existing_project(self):
        project_controller.create_project('test_project', '.')

        self.assertRaises(ProjectExistsError,
                          project_controller.create_project, 'test_project', '.')

    def test_create_fails_with_invalid_value(self):
        self.assertRaises(InvalidValueError,
                          project_controller.create_project, '', '.')

        self.assertRaises(InvalidValueError,
                          project_controller.create_project, 'test project', '')

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

    def test_read_resource_works(self):
        template = template_controller.create_template('test template',
            'test_template.tex', '~/.texviper/templates', 'test')
        project = project_controller.create_project('test_project',
            '~/.texviper/projects', template.name)
        resource = project_controller.get_resources(project.project_id)[0]

        self.assertEqual(project_controller.read_resource(
            resource.resource_id, project.project_id), 'test'
        )
