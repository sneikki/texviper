from datetime import datetime
from PySide2.QtCore import QObject, Slot, QUrl
from PySide2.QtQml import QQmlComponent
from PySide2.QtQuick import QQuickItem

from views.view import View
from controllers.project_controller import project_controller
from utils.exceptions import (
    DirectoryNotEmptyError, InvalidValueError, ProjectExistsError
)
from config.config import config

class HomeView(View):
    def __init__(self, engine):
        super().__init__(engine)

        self.component = QQmlComponent(self.engine)
        self.component.loadUrl('src/views/qml/components/PreviewCard.qml')
        self.projects_list = self.root.findChild(QQuickItem, 'projects')
        self.load_projects()

    def load_projects(self):
        projects = project_controller.get_projects()

        for project in projects:
            self.add_project(project)

    def add_project(self, project):
        item = self.component.create()
        item.setProperty('project_id', project.project_id)
        item.setProperty('name', project.name)
        item.setProperty('modified', f'Last modified: {self.timestamp_to_date(project.last_modified)}')
        item.setObjectName(project.project_id)
        item.setParentItem(self.projects_list)
        item.setParent(self.projects_list)

    def timestamp_to_date(self, timestamp):
        return str(datetime.fromisoformat(timestamp).date())

    @Slot(str, str)
    def create_project_clicked(self, name, path):
        try:
            project = project_controller.create_project(name, path)
            self.add_project(project)
        except InvalidValueError as err:
            print(err)
        except DirectoryNotEmptyError:
            print('Unable to create project: directory not empty')
        except ProjectExistsError:
            print('Unable to create project: project exists')
        except PermissionError:
            print('Unable to create project: permission denied')
        else:
            print('Project created')

    @Slot()
    def import_project_clicked(self):
        print('import project')

    @Slot(result=str)
    def get_default_path(self):
        return config.get_value('default_project_path')
        