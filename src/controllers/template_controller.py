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
        return template

    def remove_template(self, template_id):
        template_store.delete_one(template_id)

    def get_templates(self):
        return template_store.find_all()

    def get_template_names(self):
        names = list(map(lambda t: t.name, template_store.find_all()))
        return list(names)

    def get_source(self, template_id):
        return template_store.read(template_id)


template_controller = TemplateController()
