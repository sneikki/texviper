from models.project import Project
from stores.project_store import project_store
from utils.exceptions import ProjectExistsError

class ProjectController:
    """ Handles logical operations for projects
    """

    def create_project(self, name, path):
        """ Creates a new project and saves it to database and file system

        Args:
            name (string): string that represents name of the project
            path (string): string that represents path of the project
        """

        if project_store.exists(name):
            raise ProjectExistsError
        project = Project(name, path)

        project_store.create(project)

    def get_project_names(self):
        """ Returns list of names of all projects

        Returns:
            list: list of names of all projects
        """

        names = map(lambda name: name[0], project_store.find_all(['name']))
        return list(names)

    def get_projects(self):
        """ Returns list of all projects containing all fields

        Returns:
            list: list of all projects or empty list if nothing was found
        """

        projects = project_store.find_all()
        return projects

    def get_project_by_id(self, project_id):
        """ Finds and returns a single project by project_id.
            Returns None if no project with given project_id can be found.

        Args:
            project_id (string): Id of the project

        Returns:
            Project: project or None if nothing was found
        """

        project = project_store.find_one(f"project_id = '{project_id}'")
        return project

    def get_project_by_name(self, name):
        """ Finds and returns a single project by name.
            Returns None if no project with given name can be found.

        Args:
            name (string): name of the project

        Returns:
            Project: project or None if nothing was found
        """

        project = project_store.find_one(f"name = '{name}'")
        return project

    def remove_project(self, project_id):
        """ Deletes a project by project_id

        Args:
            project_id (string): id of the project to remove
        """

        project_store.delete_one(project_id)

project_controller = ProjectController()
