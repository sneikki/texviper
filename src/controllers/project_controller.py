import subprocess
from pathlib import Path

from models.project import Project
from models.resource import Resource
from controllers.template_controller import template_controller
from stores.project_store import project_store
from utils.exceptions import ProjectExistsError, InvalidValueError, BuildError
from utils.filesystem import file_system
from config.config import config

class ProjectController:
    """ Handles logical operations for projects
    """

    def create_project(self, name, path, template_name=None):
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
        root = self.add_resource(config.get_value('root_filename'), '.', 'tex',
            project.project_id, Path(project.path).expanduser() / project.name, True)
        self.add_resource('projectrc.json', '.', 'config', project.project_id, Path(
            project.path).expanduser() / 'projectrc.json')
        project_store.set_root_file(config.get_value(
            'root_filename'), project.project_id)

        if template_name:
            templates = template_controller.get_templates()
            template = list(filter(lambda t: t.name == template_name, templates))[0]

            source = template_controller.get_source(template.template_id)
            self.write_resource(root.resource_id, project.project_id, source)

        return project

    def add_resource(self, name, path, resource_type, project_id, project_path, create=False):
        """ Adds a resource to project

        Args:
            name (str): Name of the resource
            path (str): Path of the resource, relative to project
            resource_type (str): Type of the resource. Either 'tex' or 'config'
            project_id (str): Id of the project to which the resource will be added
            project_path (str): Path of the project
            create (bool, optional): Whether a file should be created to project. Defaults to False.

        Returns:
            Resource: created resource
        """
        resource = Resource(name, path, resource_type)

        project_store.add_resource(resource, project_id)

        full_path = project_path / path / name
        if create and not file_system.file_exists(full_path):
            file_system.create_directory(Path(project_path) / path)
            file_system.create_file(full_path)

        return resource

    def remove_resource(self, resource_id, project_id):
        """ Removes a resource from project

        Args:
            resource_id (str): Id of the resource to remove
            project_id (str): Id of the project that owns the resource
        """
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

    def read_resource(self, resource_id, project_id):
        """ Reads contents of a resource

        Args:
            resource_id (str): Id of the resource to read
            project_id (str): Id of the project that owns the resource

        Returns:
            str: Contents of the resource
        """
        resources = project_store.get_resources(project_id)

        resource = [
            resource for resource in resources if resource.resource_id == resource_id][0]
        project = project_store.find_by_id(project_id)
        path = Path(project[2]) / project[1] / resource.path / resource.name
        return path.read_text()

    def write_resource(self, resource_id, project_id, source):
        """ Writes text to a resource

            Args:
                resource_id (str): Id of the resource to write to
                project_id (str): Id of the project that owns the resource
                source (str): Source to write to the resource
        """
        resource = project_store.get_resource_by_id(resource_id, project_id)
        project = project_store.find_by_id(project_id)
        path = Path(project[2]) / project[1] / resource.path / resource.name
        path.write_text(source)

    def get_resources(self, project_id):
        """ Returns all resources in a project

        Args:
            project_id (str): Id of the project

        Returns:
            resources: List of resources
        """
        return project_store.get_resources(project_id)

    def remove_project(self, project_id):
        """ Deletes a project by project_id

        Args:
            project_id (string): id of the project to remove
        """

        project_store.delete_one(project_id)


    def build_project(self, project_id):
        """ Builds a PDF file from source code

            Args:
                project_id (string): id of the project to build

            Returns:
                context: Tuple containing a lambda that builds the pdf
                    and path of the generated file
        """
        root_name = project_store.get_root_resource(project_id)
        if not root_name:
            raise BuildError('Root resource missing')

        root_resource = list(
            filter(lambda res: res.name == root_name,
                project_store.get_resources(project_id)
            )
        )[0]

        project = self.get_project_by_id(project_id)

        return (
            lambda: self._build_pdf(root_resource.name,
                str(Path(project.path).expanduser() / project.name)),
            str(Path(project.path).expanduser() / project.name / 'main.pdf')
        )

    #
    #   Private
    #

    def _build_pdf(self, name, path):
        """ Builds a pdf from a given file in given path

        Args:
            name (str): Name of the file
            path (str): Path of the file
        """
        subprocess.run(['pdflatex', '-halt-on-error', name], cwd=path, check=True)

project_controller = ProjectController()
