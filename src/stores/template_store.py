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
        database.begin()

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
        template = self.find_by_id(template_id)

        if template:
            full_path = Path(template.path).expanduser() / template.filename
            return full_path.read_text()

    def write(self, template_id, source):
        template = self.find_by_id(template_id)
        self._write(template, source)

    def exists(self, name):
        query = f'''
            select template_id from Templates
            where name="{name}"
        '''

        database.execute(query)
        return len(database.fetch_all()) > 0

    def find_by_id(self, template_id):
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
        query = f'''
            insert into Templates (template_id, name, filename, path)
            values ("{template.template_id}", "{template.name}",
            "{template.filename}", "{template.path}")
        '''

        database.execute(query)

    def _write(self, template, source):
        expanded_path = Path(template.path).expanduser()

        expanded_path.mkdir(parents=True, exist_ok=True)

        full_path = expanded_path / template.filename
        file_system.write(full_path, source)


template_store = TemplateStore()
