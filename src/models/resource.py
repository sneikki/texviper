from uuid import uuid4 as uuid


class Resource:
    """ Represents a single resource in a project

        Attributes:
            name:           Name of the resource
            path:           Path of the resource, relative to project
            type:           Type of the resource
            resource_id:    Id of the resource
    """

    def __init__(self, name, path, resource_type, resource_id=None):

        self.resource_id = resource_id or str(uuid())
        self.name = name
        self.path = path
        self.type = resource_type
