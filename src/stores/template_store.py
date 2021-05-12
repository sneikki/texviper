from pathlib import Path
from sqlite3 import IntegrityError, OperationalError

from models.template import Template
from db.db_connection import database
from utils.filesystem import file_system


class TemplateStore:

    #
    #   Public
    #

    def create(self, template, source):
        """ Creates a new template

        Args:
            template (Template): Model representing template
            source (string): Source of the template

        Raises:
            err: Raised if template cannot be written to file system or database.
        """

        try:
            self._create_record(template)
            self._write(template, source)
        except (
            PermissionError,
            IntegrityError,
            OperationalError
        ) as err:
            database.rollback()
            raise err
        else:
            database.commit()

    def delete_one(self, template_id):
        """ Deletes a template by id

        Args:
            template_id (string): Id of the templat to delete
        """

        template = self.find_by_id(template_id)

        query = f'''
            delete from Templates
            where template_id="{template_id}"
        '''

        database.execute(query)
        database.commit()

        try:
            file_system.remove_file(
                Path(template.path).expanduser() / template.filename)
        except:
            pass

    def read(self, template_id):
        """ Retrieves source of a template

            Args:
                template_id (string): Id of the template

            Returns:
                string: Source of the template
        """

        template = self.find_by_id(template_id)

        if template:
            full_path = Path(template.path).expanduser() / template.filename
            return full_path.read_text()

        return None

    def write(self, template_id, source):
        """ Writes templae source to file

            Args:
                template_id (string): Id of the template
                source (string): Source of the template
        """
        template = self.find_by_id(template_id)
        self._write(template, source)

    def exists(self, name):
        """ Checks if a template with given name exists

            Args:
                name (string): Name of the template to check

            Returns:
                bool: Whether template exists
        """

        query = f'''
            select template_id from Templates
            where name="{name}"
        '''

        database.execute(query)
        return len(database.fetch_all()) > 0

    def find_by_id(self, template_id):
        """ Finds a single template by id

            Args:
                template_id (string): Id of the template

            Returns:
                template: Template object representing the template
        """

        return self.find_one(f'template_id="{template_id}"')

    def find_one(self, conditions):
        query = f'''
            select * from Templates
            where {conditions}
        '''

        database.execute(query)
        template = database.fetch_one()
        return Template(template[1], template[2], template[3], template[0])

    def find_all(self):
        """ Returns all templates

            Returns:
                templates: List of existing templates
        """

        query = '''
            select * from Templates
        '''

        database.execute(query)
        templates = database.fetch_all()

        return list(
            map(
                lambda t: Template(t[1], t[2], t[3], t[0]),
                templates
            )
        ) if templates else []

    #
    #   Private
    #

    def _create_record(self, template):
        """ Inserts the template into database

        Args:
            template (Template): Template model
        """

        query = f'''
            insert into Templates (template_id, name, filename, path)
            values ("{template.template_id}", "{template.name}",
            "{template.filename}", "{template.path}")
        '''

        database.execute(query)

    def _write(self, template, source):
        """ Writes template source to file system

            Args:
                template (Template): Template model
                source (string): Source of the templat
        """

        expanded_path = Path(template.path).expanduser()

        expanded_path.mkdir(parents=True, exist_ok=True)

        full_path = expanded_path / template.filename
        file_system.write(full_path, source)


template_store = TemplateStore()
