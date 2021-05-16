import json
from datetime import datetime
from pathlib import Path
from sqlite3 import IntegrityError, OperationalError

from models.project import Project
from db.db_connection import database
from config.config import config
from utils.filesystem import file_system
from utils.exceptions import InvalidResourceError
from stores.resource_store import resource_store


class ProjectStore:
    #
    #   Public
    #

    def create(self, project):
        """ Creates a new project

            Creates a new project by model from parameter project.
            Inserts a record into database and writes appropriate
            files to file system.

        Args:
            project (Project): project to be created
        """

        # A transaction is used to ensure that no record is
        # created in case of file system operations fail.
        database.begin()

        try:
            self._create_record(project)
            self._write(project)
        except (
            PermissionError,
            FileExistsError,
            IntegrityError,
            OperationalError
        ) as err:
            database.rollback()
            raise err
        else:
            database.commit()

    def exists(self, name):
        """ Check wheter a project with a given name
            exists in database.

            Args:
                name (string): name of the project the look for

        """

        query = f'''
            select project_id from Projects
            where name="{name}"
        '''

        database.execute(query)
        return len(database.fetch_all()) > 0

    def delete_one(self, project_id):
        """ Deletes a project by id

        Args:
            project_id (string): Id of the project to remove
        """

        project = self.find_by_id(project_id)

        query = f'''
            delete from Projects
            where project_id="{project_id}"
        '''

        database.execute(query)
        database.commit()

        if project:
            self._destruct_project(project[2], project[1])

    def open_config(self, project_id):
        """ Reads config file of a project

        Args:
            project_id (string): Id of the project

        Returns:
            config: Dictionary representing the config file. None if not found.
        """

        project = self.find_one(f'''project_id="{project_id}"''')

        if project:
            path = Path(project.path) / project.name / 'projectrc.json'
            try:
                with open(path) as config_file:
                    project_config = json.load(config_file)
                    return project_config
            except FileNotFoundError as err:
                raise InvalidResourceError from err
            except json.JSONDecodeError as err:
                raise InvalidResourceError from err
        else:
            return None

    def save_config(self, project_config):
        """ Writes configuration to config file

            Args:
                project_config (dict): Dictionary representing the configuration
        """
        path = Path(self.find_one(f'''name="{project_config['name']}"''').path)
        name = project_config['name']

        with open(path / name / 'projectrc.json', 'w') as out_file:
            json.dump(project_config, out_file, indent=4)

    def add_resource(self, resource, project_id):
        """ Adds a resource to a project

            Args:
                resource (Resource): Resource to add
                project_id (string): Id of the project that owns the resource
        """

        project_config = self.open_config(project_id)
        if not 'resources' in project_config:
            project_config['resources'] = []
        project_config['resources'].append(
            resource_store.serialize(resource))
        self.save_config(project_config)

    def update_timestamp(self, project_id, timestamp=str(datetime.now())):
        """ Updates last_modified field of a project

            Args:
                project_id (string): Id of the projcet
                timestamp (string, optional): Timestamp to set. Defaults to current time.
        """

        query = f'''
            update Projects
            set last_modified = "{timestamp}"
            where project_id="{project_id}"
        '''

        database.execute(query)
        database.commit()

    def remove_resource(self, resource_id, project_id):
        project_config = self.open_config(project_id)

        project_config['resources'] = list(
            filter(
                lambda r: r['resource_id'] != resource_id,
                project_config['resources']
            )
        )

        self.save_config(project_config)

    def set_root_file(self, filename, project_id):
        """ Sets the root file of a project

            Args:
                filename (string): File name of the root file
                project_id (string): Id of the project
        """

        project_config = self.open_config(project_id)
        project_config['root'] = filename
        self.save_config(project_config)

    def find_by_id(self, project_id):
        """ Finds a project by id

            Args:
                project_id (string): Id of the project
        """

        query = f'''
            select * from Projects
            where project_id="{project_id}"
        '''
        database.execute(query)
        return database.fetch_one()

    def find_one(self, conditions):
        """ Looks for a single project by given conditions

        Args:
            conditions (list): List of conditions for limiting the query

        Returns:
            Project: project or None if nothing was found
        """

        query = f'''
            select * from Projects
            where {conditions}
        '''

        database.execute(query)
        project = database.fetch_one()
        return Project(project[1], project[2], project[0], project[3]) if project else None

    def find_all(self):
        """ Fetches all projects from database and returns
            appropriate fields.

        Returns:
            list: list of projects or empty list if nothing was found

        """

        query = '''
            select * from Projects
        '''

        database.execute(query)
        projects = database.fetch_all()

        return list(map(
            lambda p: Project(p[1], p[2], p[0], p[3]),
            projects
        )) if projects else []

    def get_resources(self, project_id):
        """ Returns all resources of a project

            Args:
                project_id (string): Id of the project

            Returns:
                resources: List of the resources
        """

        project_config = self.open_config(project_id)

        return list(
            map(
                lambda res: resource_store.create(
                    res['name'], res['path'], res['type'], res['resource_id']),
                project_config['resources']
            )
        )

    def get_resource_by_id(self, resource_id, project_id):
        """ Finds a resoure by id in a project

            Args:
                resource_id (string): Id of the resource to find
                project_id (string): Id od the project that owns the resource

            Returns:
                resource: The resource if found. None otherwise.
        """

        resources = project_store.get_resources(project_id)

        return [resource for resource in resources
            if resource.resource_id == resource_id][0] or None

    def get_root_resource(self, project_id):
        """ Returns root resource of a project

            Args:
                project_id (string): Id of the project

            Returns:
                string: File name of the root resource
        """

        project_config = self.open_config(project_id)

        return project_config['root']

    #
    #   Private
    #

    def _create_record(self, project):
        """ Inserts project data into database

        Args:
            project (Project): data to be inserted

        """

        query = f'''
            insert into Projects (project_id, name, path, last_modified)
            values ("{project.project_id}", "{project.name}",
            "{Path(project.path).expanduser()}", "{project.last_modified}")
        '''

        database.execute(query)

    def _write(self, project):
        """ Writes project files to file system.
            Directory, if already existing, must
            be empty. Otherwise an error will be
            thrown.

        Args:
            project (Project): data to be written
        """

        expanded_path = Path(project.path).expanduser() / project.name

        self._initialize_directory(expanded_path)
        self._initialize_config(
            expanded_path, project.project_id, project.name)

    def _initialize_directory(self, path):
        """ Initializes project directory at desired location.
            If existing directory is used, it must be empty.
            Otherwise an exception will be raised

        Args:
            path (Path): Project path

        Raises:
            FileExistsError: if existing directory is not empty
        """

        if file_system.directory_exists(path) and not file_system.directory_empty(path):
            raise FileExistsError()

        file_system.create_directory(path)

    def _initialize_config(self, path, project_id, name):
        """ Adds project configuration to project directory

        Args:
            path (Path): project path
            project_id (string): id of the project to store in the config
            name (string): name of the project to store in the config
        """

        config_str = config.create_project_config(project_id, name)
        full_path = path / 'projectrc.json'

        file_system.create_file(full_path)
        file_system.write(full_path, config_str)

    def _destruct_project(self, path, name):
        """ Removes all project resources from file system

        Args:
            path (Path): Project path
            name (string): Project name
        """

        full_path = Path(path) / name

        try:
            file_system.remove_directory(full_path)
        except (FileNotFoundError, PermissionError):
            pass


project_store = ProjectStore()
