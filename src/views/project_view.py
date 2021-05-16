from pathlib import Path
from PySide2.QtCore import QObject, Slot, QUrl
from PySide2.QtQml import QQmlComponent

from views.view import View
from views.build_thread import BuildThread
from controllers.project_controller import project_controller
from config.config import config
from utils.exceptions import BuildError, InvalidResourceError
from utils.literal import get_literal


class ProjectView(View):
    def __init__(self, engine):
        super().__init__(engine)

        self.open_projects = []
        self.tabs = {}
        self.current = None
        self.project_stack = self.root.findChild(QObject, 'projectStack')
        self.project_view = self.root.findChild(QObject, 'projectView')
        self.tab_bar = self.root.findChild(QObject, 'projectsTab')
        self.build_thread = None

        self.components = {
            'editor_view': QQmlComponent(self.engine,
                                         QUrl('src/views/qml/EditorView.qml')),
            'project_tab': QQmlComponent(self.engine,
                                         QUrl('src/views/qml/components/ProjectTab.qml')),
            'resource_entry': QQmlComponent(self.engine,
                                            QUrl('src/views/qml/components/ResourceEntry.qml'))
        }

    def is_project_open(self, project_id):
        """ Checks if a project with given id is open.

            Args:
                project_id (string): Id of the project to check

            Returns:
                bool: Whether the project is open
        """
        return len([project for project in self.open_projects
                    if project.project_id == project_id]) > 0

    def find_editor(self, project_id):
        """ Finds an editor object in the editor and
            returns that object.

            Args:
                project_id (string): Id of the projec to find

            Returns:
                object: Object representing the editor object
        """
        return self.project_stack.find_editor(project_id)

    def load_resources(self, project_id):
        """ Loads all resources that belong in a project
            and creates entries for them in the resource panel.

            Args:
                project_id (string): Id of the project
        """
        resources = project_controller.get_resources(project_id)
        editor = self.find_editor(project_id)

        for resource in resources:
            editor.add_resource(resource.name, resource.resource_id)

    def create_editor_view(self, project):
        """ Creates a view for a project in the editor.

            Args:
                project (Project): project model
        """
        self.project_stack.add_editor_view(project.name, project.project_id)

        # Add tab
        tab = self.components['project_tab'].create()
        tab.setProperty('text', project.name)
        tab.setProperty('project_id', project.project_id)
        self.tab_bar.addItem(tab)
        self.tabs[project.project_id] = tab

    @Slot(str)
    def open_project(self, project_id):
        """ Opens a project in project view. Shows an error message
            if project can't be opened.

            Args:
                project_id (string): Id of the projet to open
        """
        windows_layout = self.root.findChild(QObject, 'windowsLayout')
        windows_layout.set_current(1)

        if self.is_project_open(project_id):
            return

        project = project_controller.get_project_by_id(project_id)
        self.open_projects.append(project)

        self.create_editor_view(project)

        try:
            self.load_resources(project_id)
        except InvalidResourceError:
            self.show_error(
                'Error',
                f"{get_literal('failed_to_open_project')}: {get_literal('invalid_resource')}"
            )
            self.close_project(project.project_id)
        else:
            self.project_view.setProperty(
                'projectCount', len(self.open_projects))
            if not self.current:
                self.current = project_id

    @Slot(str)
    def show_project(self, project_id):
        """ Called when open project button is clicked.
            Opens the project and changes view to project view.

            Args:
                project_id (string): Id of the project
        """
        self.project_stack.show_project(project_id)

        self.current = project_id

    @Slot(str, str)
    def open_resource(self, name, resource_id):
        """ Called when a resource is requested to be opened.

            Args:
                name (string): Name of the resource
                resource_id (string): Id of the resource
        """
        try:
            source = project_controller.read_resource(
                resource_id, self.current)
        except FileNotFoundError:
            self.show_error(
                'Error',
                f"{get_literal('failed_to_open_resource')}: {get_literal('file_missing')}"
            )
        else:
            editor = self.find_editor(self.current)
            editor.open_resource(name, source, resource_id)

    @Slot(str)
    def show_resource(self, resource_id):
        """ Changes an open resource to the currently
            open resource.

            Args:
                resource_id (string): Id of the resource
        """
        editor = self.find_editor(self.current)
        editor.show_resource(resource_id)

    @Slot(str)
    def close_resource(self, resource_id):
        """ Closes the view of an open resource.

            Args:
                resource_id (string): Id of the resource to close
        """
        editor = self.find_editor(self.current)
        editor.close_resource(resource_id)

    @Slot(str)
    def add_resource(self, name):
        """ Called when a new resource is being added to a project.

            Args:
                name (string): Name of the new resource
        """
        file_name = name + '.tex' if not name.endswith('.tex') else name
        project = project_controller.get_project_by_id(self.current)
        resource = project_controller.add_resource(file_name, '.', 'tex',
                                                   self.current, Path(project.path) / project.name, True)

        editor = self.find_editor(self.current)
        editor.add_resource(resource.name, resource.resource_id)

    @Slot(str)
    def remove_resource(self, resource_id):
        """ Removes an existing resource from a projcet.

            Args:
                resource_id (string): Id of the resource to remove
        """
        project_controller.remove_resource(resource_id, self.current)

        editor = self.find_editor(self.current)
        editor.remove_resource(resource_id)

    @Slot()
    def save_resource(self):
        """ Writes contents of the currently visible resource to a file.
        """
        editor = self.find_editor(self.current)

        source = editor.get_open_resource_contents()
        resource_id = editor.get_open_resource_id()
        project_controller.write_resource(resource_id, self.current, source)

    @Slot()
    def close_project(self, project_id=None):
        """ Closes a project.

            Args:
                project_id (string, optional): Id of the project to close.
                    If nothing is given, the currently open project will be closed.
        """
        if len(self.open_projects) == 0:
            return

        if not project_id:
            project_id = self.current

        editor = self.find_editor(project_id)
        editor.deleteLater()

        # Remove tab
        tab = self.tabs[project_id]
        tab.deleteLater()
        self.tabs[project_id] = None

        self.open_projects = list(
            filter(lambda p: p.project_id != project_id, self.open_projects))

        if len(self.open_projects) >= 1:
            self.current = self.open_projects[-1].project_id
            self.show_project(self.current)
        else:
            self.current = None

    def refresh(self, url, state):
        """ Refreshses the preview view if compilation succeeded. Otherwise
            shows an error message.

            Args:
                url (string): Url of the file to show
                state (bool): Whether compilation was successful
        """
        if state:
            editor = self.find_editor(self.current)
            editor.update_preview(url)
        else:
            self.show_error(
                'Error', 'Compilation failed. No output generated.')

    @Slot()
    def build_project(self):
        """ Builds the currently open project. Fetches a callback from
            project controller and call that in another thread without blocking ui.
        """
        if self.current:
            build_ctx = project_controller.build_project(self.current)
            self.build_thread = BuildThread(
                build_ctx[0], lambda state: self.refresh(build_ctx[1], state)
            )
            self.build_thread.start()

    @Slot(result=str)
    def get_font(self):
        """ Gets the editor font specified in config.

            Returns:
                string: Editor font
        """
        return config.get_value('editor_font')
