from uuid import uuid4 as uuid


class Project:  # pylint: disable=too-few-public-methods
    """ Represents a single project

        Attributes:
            name:       Name of the project
            path:       Path of the project
            project_id: Unique identifier of the project
    """

    def __init__(self, name, path, project_id=None):
        """ Creates a new project

        Args:
            name (string): String that represents name of the project
            path (string): String that represents path of the project
            project_id ([string], optional): [description]. String that represents if
                of the project. Defaults to None, in that case id is auto-generated.
        """

        self.project_id = project_id or str(uuid())
        self.name = name
        self.path = path
