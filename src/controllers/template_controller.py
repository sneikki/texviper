from models.template import Template
from stores.template_store import template_store
from utils.exceptions import InvalidValueError

class TemplateController:
    def create_template(self, name, filename, path, source):
        if not name:
            raise InvalidValueError('Invalid name')
        if not filename:
            raise InvalidValueError('Invalid filename')
        if not path:
            raise InvalidValueError('Invalid path')

        if template_store.exists(name):
            raise FileExistsError

        template = Template(name, filename, path)
        template_store.create(template, source)

template_controller = TemplateController()
