from models.template import Template
from stores.template_store import template_store
from utils.exceptions import InvalidValueError


class TemplateController:
    def create_template(self, name, filename, path, source):
        """ Creates a new template and writes it to
            appropriate location.

        Args:
            name (string): Name of the template
            filename (string): File name of the template
            path (string): Path of the template in file system
            source (string): Source code of the template

        Raises:
            InvalidValueError: Raised if name, file name or path is invalid
            FileExistsError: Raised if template with given name exists

        Returns:
            Template: created template
        """

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
        """ Removes a template by template id

        Args:
            template_id (string): Id of the template to be removed
        """
        template_store.delete_one(template_id)

    def get_templates(self):
        """ Returns a list of all templates

            Returns:
                templates: list of templates
        """
        return template_store.find_all()

    def get_template_names(self):
        """ Returns a list of names of all templates

            Returns:
                names: list of names
        """

        names = list(map(lambda t: t.name, template_store.find_all()))
        return list(names)

    def get_source(self, template_id):
        """ Returns the source code of a single template

            Returns:
                source: Source of the template
        """
        return template_store.read(template_id)


template_controller = TemplateController()
