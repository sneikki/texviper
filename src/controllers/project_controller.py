from models.project import Project
from stores.project_store import project_store


class ProjectController:  # pylint: disable=too-few-public-methods
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


project_controller = ProjectController()
