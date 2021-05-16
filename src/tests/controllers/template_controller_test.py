from pathlib import Path
from pyfakefs import fake_filesystem_unittest

from controllers.template_controller import template_controller
from config.config import config
from db.db_connection import database
from utils.exceptions import InvalidValueError


class TemplateControllerTest(fake_filesystem_unittest.TestCase):
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
        template_controller.create_template('test template',
                                            'test_template.tex', '~/.texviper/templates', '')

    def test_create_fails_with_existing_template(self):
        template_controller.create_template('test template',
                                            'test_template.tex', '~/.texviper/templates', '')

        self.assertRaises(FileExistsError,
                          template_controller.create_template, 'test template',
                          'test_template.tex', '~/.texviper/templates', ''
                          )

    def test_create_fails_with_invalid_values(self):
        self.assertRaises(InvalidValueError,
                          template_controller.create_template, '', 'test_template.tex', '~/.texviper/templates', '')

        self.assertRaises(InvalidValueError,
                          template_controller.create_template, 'test template', '', '~/.texviper/templates', '')

        self.assertRaises(InvalidValueError,
                          template_controller.create_template, 'test template', 'test_template.tex', '', '')

    def test_source_is_written_to_file(self):
        source = '''\\documentclass{article}
\\begin{document}
\\end{document}'''

        template_controller.create_template('test template',
                                            'test_template.tex', '~/.texviper/templates', source)

        self.assertEqual(
            Path('~/.texviper/templates/test_template.tex').expanduser().read_text(),
            source
        )

    def test_get_templates_returns_all_templates(self):
        template_controller.create_template('template 1',
                                            'template_1.tex', '~/.texviper/templates', '')
        template_controller.create_template('template 2',
                                            'template_2.tex', '~/.texviper/templates', '')
        template_controller.create_template('template 3',
                                            'template_3.tex', '~/.texviper/templates', '')

        self.assertEqual(len(template_controller.get_templates()), 3)

    def test_get_source_works_correctly(self):
        source = '''\\documentclass{article}
\\begin{document}
\\end{document}'''

        template = template_controller.create_template('test template',
                                                       'test_template.tex', '~/.texviper/templates', source)

        self.assertEqual(template_controller.get_source(
            template.template_id), source)

    def remove_template_removes_template(self):
        template = template_controller.create_template('test template',
                                                       'test_template.tex', '~/.texviper/templates', '')

        template_controller.remove_template(template.template_id)
        self.assertEqual(len(template_controller.get_templates()), 0)
