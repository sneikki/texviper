from pathlib import Path

from config.config import config

class CreateProjectError(Exception):
    pass


class ProjectStore:  # pylint: disable=too-few-public-methods
    def __init__(self):
        self.projectrc_name = "projectrc.json"  # for now

    def create_project(self, project):
        path = Path(project.path) / project.name

        if self._create_directory(path):
            self._init_project(project)

    def _create_directory(self, path):
        try:
            path.mkdir(parents=True)
        except PermissionError as permission_error:
            raise CreateProjectError("Permission denied") from permission_error
        except FileExistsError as exists_error:
            raise CreateProjectError("Directory exists") from exists_error

        return True

    def _init_project(self, project):
        rc_path = Path(project.path) / project.name / self.projectrc_name

        rc_path.touch()

        project_rc = config.create_project_config(project)
        rc_path.write_text(project_rc)


project_store = ProjectStore()
