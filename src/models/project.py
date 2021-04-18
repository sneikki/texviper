from uuid import uuid4 as uuid
from datetime import datetime

class Project:
    """ Represents a single project

        Attributes:
            name:           Name of the project
            path:           Path of the project
            project_id:     Unique identifier of the project
            last_modified:  Timestamp of last modification to project
    """

    def __init__(self, name, path, project_id=None, last_modified=None):
        """ Creates a new project

        Args:
            name (string): String that represents name of the project
            path (string): String that represents path of the project
            project_id ([string], optional): String that represents if
                of the project. Defaults to None, in that case id is auto-generated.
            last_modified ([string], optional): String that represents timestamp of last
                modification of the project.
        """

        self.project_id = project_id or str(uuid())
        self.name = name
        self.path = path
        self.last_modified = last_modified or str(datetime.now())
