from models.resource import Resource

class ResourceStore:
    
    def create(self, name, path, resource_type, resource_id=None):
        return Resource(resource_id, name, path, resource_type)

    def find_all_in_project(self, project_id):
        pass

    def find_in_project(self, resource_id, project_id):
        pass

    def serialize(self, resource):
        return { 'resource_id': resource.resource_id, 'name': resource.name, 'path': resource.path, 'type': resource.type }

resource_store = ResourceStore()
