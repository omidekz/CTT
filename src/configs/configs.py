from pydantic import BaseSettings
import os


class Config(BaseSettings):
    project_root: str = os.path.abspath(os.curdir)
    db_name: str = 'tasks'

    @property
    def db_url(self):
        return self.project_root + '/db.sqlite3'


configs = Config()
