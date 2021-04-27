from pathlib import Path

from models.project import Project
from models.resource import Resource
from stores.project_store import project_store
from utils.exceptions import ProjectExistsError, InvalidValueError
from config.config import config
from utils.filesystem import file_system

class ProjectController:
    """ Handles logical operations for projects
    """

    def create_project(self, name, path):
        """ Creates a new project and saves it to database and file system

        Args:
            name (string): string that represents name of the project
            path (string): string that represents path of the project
        """

        if not name:
            raise InvalidValueError('Invalid name')
        if not path:
            raise InvalidValueError('Invalid path')

        if project_store.exists(name):
            raise ProjectExistsError
        project = Project(name, path)

        project_store.create(project)
        self.add_resource(config.get_value('root_filename'), '.', 'root', project.project_id, Path(project.path).expanduser() / project.name, True)
        project_store.set_root_file(config.get_value('root_filename'), project.project_id)

        return project

    def add_resource(self, name, path, resource_type, project_id, project_path, create=False): # _todo: error handling
        resource = Resource(name, path, resource_type)

        project_store.add_resource(resource, project_id)

        full_path = project_path / path / name
        if create and not file_system.file_exists(full_path):
            file_system.create_directory(Path(project_path) / path)
            file_system.create_file(full_path)

    def remove_resource(self, resource_id, project_id):
        project_store.remove_resource(resource_id, project_id)

    def get_project_names(self):
        """ Returns list of names of all projects

        Returns:
            list: list of names of all projects
        """

        names = list(map(lambda p: p.name, project_store.find_all()))
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

        project = project_store.find_one(f'project_id = "{project_id}"')
        return project

    def get_project_by_name(self, name):
        """ Finds and returns a single project by name.
            Returns None if no project with given name can be found.

        Args:
            name (string): name of the project

        Returns:
            Project: project or None if nothing was found
        """

        project = project_store.find_one(f'name = "{name}"')
        return project

    def remove_project(self, project_id):
        """ Deletes a project by project_id

        Args:
            project_id (string): id of the project to remove
        """

        project_store.delete_one(project_id)

project_controller = ProjectController()
