from uuid import uuid4 as uuid

class Template:
    """ Represents a template to used for resource initialization

        Attributes:
            name:           name of the template
            filename:       name of the template in file system
            path:           path of the template in file system
            template_id:    unique identifier of the template
    """
    
    def __init__(self, name, filename, path, template_id=None):

        self.template_id = template_id or str(uuid())
        self.name = name
        self.filename = filename
        self.path = path
