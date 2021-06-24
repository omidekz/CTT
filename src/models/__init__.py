from .task_state import TaskState
from pydantic import BaseModel
from datetime import datetime, timedelta
import typing
from configs import Sqlite
from .time_session import Timer
from .task import Task

cur = Sqlite.cursor()
cur.executescript(
    """
        CREATE TABLE IF NOT EXISTS Tasks (
            id INTEGER PRIMARY KEY,
            label TEXT NOT NULL,
            state TEXT,
            total_time INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS Times (
            id INTEGER PRIMARY KEY,
            start TEXT NOT NULL,
            end TEXT,
            task_id INTEGER NOT NULL,
            FOREIGN KEY (task_id) 
                REFERENCES tasks (id)
                ON DELETE CASCADE
        );
        PRAGMA foreign_keys = ON;
    """
)

