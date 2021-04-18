from db.db_connection import database, DatabaseConnectionError
from config.config import config, ConfigError

class Application:
    def __init__(self):
        pass

    def run(self):
        config.open_config()
        try:
            database.connect()
        except DatabaseConnectionError as db_err:
            raise db_err
    