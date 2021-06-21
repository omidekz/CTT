from pydantic import BaseModel
from enum import Enum
import typing
from datetime import datetime, timedelta
from configs import Sqlite


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
            FOREIGN KEY (task_id) REFERENCES tasks (id)
        )
    """
)


class TaskState(str, Enum):
    DONE = 'done'
    IN_PROGRESS = 'progress'
    TODO = 'todo'


class Timer(BaseModel):
    start: datetime
    end: typing.Optional[datetime]

    @property
    def duration(self) -> timedelta:
        return (self.end or datetime.now()) - self.start


class Task(BaseModel):
    label: str
    state: TaskState = TaskState.TODO
    times: typing.List[Timer] = []
    id: int = None
    _total_time: int = -1

    def __init__(self, **kwargs):
        db = kwargs.pop('db', True)
        super(Task, self).__init__(**kwargs)
        if db:
            cur = Sqlite.cursor()
            id = cur.execute(
                f"""
                    INSERT INTO Tasks (label, state, total_time) VALUES ('{self.label}', '{self.state}', 0)
                """
            ).lastrowid
            cur.connection.commit()
            self.id = id

    @property
    def total_time(self):
        return sum(map(lambda x: x.duration, self.times))

    @classmethod
    def tasks(cls, ids: list):
        cur = Sqlite.cursor()
        query = """
            SELECT id, label, state, total_time FROM Tasks
        """
        if ids:
            operator = 'IN'
            if len(ids) == 1:
                ids = ids[0]
                operator = '='
            query += f'WHERE id {operator} {ids}'

        result = cur.execute(query).fetchall()
        return [
           Task(
               id=r[0],
               label=r[1],
               state=TaskState(r[2]),
               _total_time=r[3],
               db=False
           ) for r in result
        ]

    @classmethod
    def remove(cls, items: typing.Sequence[typing.Union[int, str]]):
        print(items)
        ids = tuple(int(i) for i in items if i.isdigit())
        if len(ids) == 1:
            ids = ids[0]
        names = [i for i in items if not not i.isdigit()]
        cur = Sqlite.cursor()
        query = f"""
                DELETE FROM Tasks
                WHERE id {isinstance(ids, tuple) and "IN" or "="} {ids};
            """
        cur.executescript(query)
        cur.connection.commit()
