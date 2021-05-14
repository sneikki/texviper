import dateutil.parser
from PySide2.QtCore import QObject, Slot
from PySide2.QtQml import QQmlComponent
from PySide2.QtQuick import QQuickItem

from views.view import View
from controllers.project_controller import project_controller
from controllers.template_controller import template_controller
from utils.exceptions import (
    DirectoryNotEmptyError, InvalidValueError, ProjectExistsError
)
from config.config import config
from utils.literal import get_literal


class HomeView(View):
    def __init__(self, engine):
        super().__init__(engine)

        self.component = QQmlComponent(self.engine)
        self.component.loadUrl('src/views/qml/components/PreviewCard.qml')
        self.projects_list = self.root.findChild(QQuickItem, 'projects')
        self.project_to_remove = None
        self.load_projects()

    def load_projects(self):
        """ Loads existing projets to ui
        """
        projects = project_controller.get_projects()

        for project in projects:
            self.add_project(project)

    def add_project(self, project):
        """ Adds a project entry to ui

            Args:
                project (Project): Project model
        """

        item = self.component.create()
        item.setProperty('project_id', project.project_id)
        item.setProperty('name', project.name)
        item.setProperty(
            'modified', f'Last modified: {self.timestamp_to_date(project.last_modified)}')
        item.setObjectName(project.project_id)
        item.setParentItem(self.projects_list)
        item.setParent(self.projects_list)

    def timestamp_to_date(self, timestamp):
        """ Converts a ISO 8601 date to datetime object

        Args:
            timestamp (string): ISO 8601 date representation

        Returns:
            datetime: Created datetime object
        """

        return dateutil.parser.isoparse(timestamp).strftime('%m-%d-%Y %H:%M')

    @Slot(str, str, str)
    def create_project_clicked(self, name, path, template_name):
        """ Callback to create project

        Args:
            name (string): Name that user entered
            path (string): Path that user entered
            template_name (string): Template name
        """
        try:
            project = project_controller.create_project(
                name, path, template_name)
            self.add_project(project)
        except InvalidValueError as err:
            self.show_error(get_literal('project_creation_failed'), str(err))
        except DirectoryNotEmptyError:
            self.show_error(get_literal('project_creation_failed'), get_literal('dir_not_empty'))
        except ProjectExistsError:
            self.show_error(get_literal('project_creation_failed'), get_literal('projects_already_exists'))
        except PermissionError:
            self.show_error(get_literal('project_creation_failed'), get_literal('permission_denied'))

    @Slot(result=str)
    def get_default_path(self):
        """ Returns default project path to ui

        Returns:
            string: Default path
        """
        return config.get_value('default_project_path')

    @Slot(str)
    def request_project_removal(self, project_id):
        """ Called when user would like to remove a project.
            Shows a confirmation dialog to the user.

            Args:
                project_id (string): Id of the project to remove
        """
        self.project_to_remove = project_id
        project = project_controller.get_project_by_id(project_id)
        if not project:
            return

        child = self.root.findChild(QObject, 'confirmRemovalDialog')
        child.setProperty('visible', True)

        child.setProperty(
            'text', f'Do you want to remove project {project.name}?')

    @Slot(result=str)
    def remove_confirmed(self):
        """ Called when user has confirmed project removal dialog.

            Returns:
                string: Id of the project to remove
        """
        project_controller.remove_project(self.project_to_remove)

        child = self.root.findChild(QQuickItem, self.project_to_remove)
        child.deleteLater()

        return self.project_to_remove

    @Slot()
    def load_templates(self):
        """ Fetches all templates and returns a list of their names.

            Returns:
                string: list of names of the templates
        """
        templates = template_controller.get_template_names()

        dropdown = self.root.findChild(QObject, 'templateDropdown')
        dropdown.set_model([''] + templates)
