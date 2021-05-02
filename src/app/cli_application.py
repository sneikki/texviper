import sys

from app.application import Application
from db.db_connection import DatabaseConnectionError
from cli import cli


class CliApplication(Application):
    def __init__(self):
        super().__init__()

    def run(self):
        try:
            super().run()
        except DatabaseConnectionError as db_err:
            print(db_err)
            sys.exit(-1)
        cli.run()
