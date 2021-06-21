import os
import sqlite3
from .configs import configs


class Sqlite:
    connection = None

    @classmethod
    def get_connection(cls, db_url: str = configs.db_url):
        if not cls.connection:
            cls.connection = sqlite3.connect(db_url)
        return cls.connection

    @classmethod
    def cursor(cls) -> sqlite3.Cursor:
        return cls.get_connection().cursor()
