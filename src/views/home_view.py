from PySide2.QtCore import QObject, Slot, QUrl
from PySide2.QtQml import QQmlComponent
from PySide2.QtQuick import QQuickItem

from controllers.project_controller import project_controller
from utils.exceptions import (
    DirectoryNotEmptyError, InvalidValueError, ProjectExistsError
)

class HomeView(QObject):
    def __init__(self):
        super().__init__()

    @Slot(str, str)
    def create_project_clicked(self, name, path):
        try:
            project_controller.create_project(name, path)
        except InvalidValueError as e:
            print(e)
        except DirectoryNotEmptyError:
            print("Unable to create project: directory not empty")
        except ProjectExistsError:
            print("Unable to create project: project exists")
        except PermissionError:
            print("Unable to create project: permission denied")
        else:
            print("Project created")

    @Slot()
    def import_project_clicked(self):
        print("import project")

