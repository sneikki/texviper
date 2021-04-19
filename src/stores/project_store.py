from pathlib import Path
from sqlite3 import (
    IntegrityError, OperationalError
)

from db.db_connection import database
from config.config import config
from utils.exceptions import DirectoryExistsError
from utils.filesystem import file_system

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
            DirectoryExistsError,
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

        query = f"""
            select project_id from Projects
            where name="{name}"
        """

        database.execute(query)
        return len(database.fetch_all()) > 0

    def delete_one(self):
        pass

    def delete_many(self):
        pass

    def find_one(self, fields, conditions):
        """ Looks for a single project by given conditions
            and returns appropriate fields.

        Args:
            fields (list): List of fields to be queried
            conditions (list): List of conditions for limiting the query
        
        Returns:
            Project: project or None if nothing was found
        """

        query = f"""
            select {database.concatenate_fields(fields)} from Projects
            where {database.construct_condition(conditions)}
        """

        database.execute(query)
        return database.fetch_one()

    def find_all(self, fields):
        """ Fetches all projects from database and returns
            appropriate fields.

        Args:
            fields (list): List of fields to be queried

        Returns:
            list: list of projects or empty list if nothing was found 

        """

        query = f"""
            select {database.concatenate_fields(fields)} from Projects
        """

        database.execute(query)
        return database.fetch_all()

    #
    #   Private
    #

    def _create_record(self, project):
        """ Inserts project data into database

        Args:
            project (Project): data to be inserted

        """

        query = f"""
            insert into Projects (project_id, name, path, last_modified)
            values ("{project.project_id}", "{project.name}",
            "{project.path}", "{project.last_modified}")
        """

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
        self._initialize_config(expanded_path, project.project_id, project.name)

    def _initialize_directory(self, path):
        """ Initializes project directory at desired location.
            If existing directory is used, it must be empty.
            Otherwise an exception will be raised

        Args:
            path (Path): Project path

        Raises:
            DirectoryExistsError: if existing directory is not empty
        """

        if file_system.directory_exists(path) and not file_system.directory_empty(path):
                raise DirectoryExistsError()
        
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

project_store = ProjectStore()
