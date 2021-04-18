from pathlib import Path
import shutil
from sqlite3 import IntegrityError

from config.config import config
from db.db_connection import database
from utils.literal import literals

class CreateProjectError(Exception):
    pass

class ProjectStore:
    def __init__(self):
        self.projectrc_name = "projectrc.json"  # for now

    def create_project(self, project):
        path = Path(project.path) / project.name
        self._create_record(project)

        try:
            self._create_directory(path)
            self._init_project(project)
        except CreateProjectError as err:
            database.rollback()
            raise err
        else:
            database.commit()

    def change_project(self, new_data):
        pass

    def remove_project_by_id(self, project_id, remove_dir=True):
        if remove_dir:
            # Query project path and remove directory

            query = f"""
                select name, path from Projects
                where project_id="{project_id}"
            """
            database.execute(query)
            res = database.fetch_one()
            name = res[0]
            path = res[1]

            # Exception about nonexistent directory can be safely ignored since
            # nothing needs to be done if the directory has already been removed
            try:
                shutil.rmtree(Path(path) / name)
            except Exception:
                pass

        query = f"""
            delete from Projects
            where project_id="{project_id}"
        """

        database.execute(query)
        database.commit()

    def remove_project_by_name(self, name):
        query = f"""
            select project_id from Projects
            where name="{name}"
        """

        database.execute(query)
        project_id = database.fetch_one()[0]

        self.remove_project_by_id(project_id)

    def find_one(self):
        pass

    def find_all(self, fields=None):
        query_fields = ','.join(fields) if fields else '*'

        query = f"""
            select {query_fields} from Projects
        """

        database.execute(query)
        return database.fetch_all()

    def _create_directory(self, path):
        try:
            path.mkdir(parents=True)
        except PermissionError as permission_error:
            raise CreateProjectError(literals['permission_denied']) from permission_error
        except FileExistsError as exists_error:
            raise CreateProjectError(literals['dir_exists']) from exists_error

    def _init_project(self, project):
        rc_path = Path(project.path) / project.name / self.projectrc_name

        rc_path.touch()

        project_rc = config.create_project_config(project)
        rc_path.write_text(project_rc)

    def _create_record(self, project):
        # Use a transaction to ensure that no database record is
        # created if creation of project files fails
        query = f"""
            begin;
            insert into Projects (project_id, name, path, last_modified)
            values ("{project.project_id}", "{project.name}", "{project.path}", "{project.last_modified}")
        """

        try:
            database.execute_script(query)
        except IntegrityError as err:
            raise CreateProjectError(literals['project_already_exists']) from err

project_store = ProjectStore()
