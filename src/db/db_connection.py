import sqlite3
from sqlite3 import OperationalError
from pathlib import Path

from config.config import config
from utils.literal import literals
from utils.exceptions import DatabaseConnectionError

class Database:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self, path=None):
        db_path = Path(config.get_value('db_path')).expanduser()
        db_name = config.get_value('db_name')
        
        full_path = path or (db_path / db_name)

        try:
            db_path.mkdir(parents=True,exist_ok=True)
            self.connection = sqlite3.connect(str(full_path))
            self.cursor = self.connection.cursor()

            with open('src/db/init_db.sql') as init_db:
                init_db_src = init_db.read()

            self.cursor.executescript(init_db_src)
        except OperationalError as err:
            raise DatabaseConnectionError(f'''{literals['database_connection_failed']}: {full_path}''') from err

    def close(self):
        if self.connection:
            self.connection.close()

    def execute(self, query):
        self.cursor.execute(query)

    def execute_script(self, script):
        self.cursor.executescript(script)

    def begin(self):
        self.cursor.execute('begin')

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def fetch_all(self):
        return self.cursor.fetchall()

    def fetch_one(self):
        return self.cursor.fetchone()

    def concatenate_fields(self, fields):
        return ','.join(fields) if fields else '*'

database = Database()
