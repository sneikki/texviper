from models.project import Project
from stores.project_store import project_store


class ProjectController:
    """ Handles logical operations for projects
    """

    def create_project(self, name, path):
        """ Creates a new project

        Args:
            name (string): String that represents name of the project
            path (string): String that represents path of the project
        """

        project = Project(name, path)

        project_store.create_project(project)

    def get_project_names(self):
        names = map(lambda name: name[0], project_store.find_all(['name']))
        return names

    def remove_project(self, name):
        project_store.remove_project_by_name(name)

project_controller = ProjectController()
