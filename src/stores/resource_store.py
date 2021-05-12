from models.resource import Resource

class ResourceStore:
    def create(self, name, path, resource_type, resource_id=None):
        """ Creates a new resource

            Args:
                name (string): Name of the resource
                path (string): Path of the resource
                resource_type (string): Type of the resource
                resource_id (string): Id of the resource

            Returns:
                resource: Created resource
        """

        return Resource(name, path, resource_type, resource_id)

    def serialize(self, resource):
        """ Serializes a resource to be written into a file

            Args:
                resource (Resource): Resource to serialize

            Returns:
                resource: Serialized resource, as a dictionary
        """

        return {'resource_id': resource.resource_id, 'name': resource.name,
            'path': resource.path, 'type': resource.type}

resource_store = ResourceStore()
