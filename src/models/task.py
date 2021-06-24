import re
import sqlite3

from . import TaskState, BaseModel, Sqlite, typing, datetime, Timer


get_value_by_custom_key = lambda key: \
                                lambda val, default: \
                                val[key] if isinstance(val, dict) else default


def convert_to_time_string(start: datetime, end: datetime):
    delta = end - start
    minute = delta.seconds // 60 + delta.days * 24 * 60
    hour, minute = minute // 60, minute % 60
    append = lambda _str, duration, char: f'{_str}{duration}{char}' if duration > 0 else _str
    return append(
        append(
            '',
            hour,
            'h'
        ),
        minute,
        'm'
    )


class Task(BaseModel):
    label: str
    # hold total time in second
    total_time_seconds: int = 0
    state: TaskState = TaskState.TODO
    times: typing.List[Timer] = []
    id: int = None

    def __init__(self, **kwargs):
        db = kwargs.pop('db', True)
        super().__init__(**kwargs)
        if db:
            cur = Sqlite.cursor()
            id = cur.execute(
                f"""
                    INSERT INTO Tasks (label, state, total_time) 
                    VALUES ('{self.label}', '{self.state}', {self.total_time_seconds})
                """
            ).lastrowid
            cur.connection.commit()
            self.id = id

    @property
    def total_time(self):
        return self.convert_sec_to_timestring(seconds=self.total_time_seconds)

    @staticmethod
    def convert_sec_to_timestring(
            start: datetime = None,
            end: datetime = None,
            seconds: int = 0
    ):
        if start and end:
            delta = end - start
            return Task.convert_sec_to_timestring(
                seconds=int(delta.total_seconds())
            )
        hour, minute = (seconds // (60 * 60)), (seconds // 60) % 60
        append = lambda _str, duration, char: f'{_str}{duration}{char}' if duration > 0 else _str
        string = ''
        string = append(string, minute, 'm')
        string = append(string, hour, 'h')
        return string

    @staticmethod
    def is_timestring(string: str):
        return bool(re.fullmatch(r'([0-9]+[mh])+', string))

    @staticmethod
    def convert_timestring_to_sec(string: str):
        if not Task.is_timestring(string):
            raise ValueError(f'{string} is not valid time_string')
        # 10h43m
        # 10h -> 10 * 60 * 60
        # 43m -> 43 * 60
        to_second = lambda x: int(x[:-1]) * 60 * 60 if 'h' in x else int(x[:-1]) * 60
        return sum(
            map(
                to_second,
                re.findall(r'(\d+[mh])', string)
            )
        )

    @classmethod
    def tasks(cls, ids: list):
        query = """
            SELECT id, label, state, total_time FROM Tasks
        """
        if ids:
            operator = 'IN'
            if len(ids) == 1:
                ids = ids[0]
                operator = '='
            query += f'WHERE id {operator} {ids}'
        result = Sqlite.simple_execute(query)
        return [
           Task(
               id=r[0],
               label=r[1],
               state=TaskState(r[2]),
               total_time_seconds=r[3],
               db=False
           ) for r in result
        ]

    @staticmethod
    def _inline_format():
        return {
            'id': '{:<5}',
            'label': {
                'format': '{:<10}',
                'name': 'name'
            },
            'state': '{:<12}',
            'time_string': {
                'format': '{:<9}',
                'name': 'payed time'
            }
        }

    @property
    def time_string(self):
        return self.convert_sec_to_timestring(seconds=self.total_time_seconds)

    @staticmethod
    def headline():
        get_name = get_value_by_custom_key('name')
        get_format = get_value_by_custom_key('format')
        return ' '.join(
            get_format(v, default=v).format(get_name(v, default=k))
            for k, v in Task._inline_format().items()
        )

    def to_inline(self):
        get_format = get_value_by_custom_key('format')
        get_value = lambda x: x() if callable(x) else x
        return ' '.join(
            get_format(v, default=v).format(get_value(getattr(self, k)))
            for k, v in Task._inline_format().items()
        )

    @classmethod
    def remove(cls, items: typing.Sequence[typing.Union[int, str]]):
        print(items)
        operator = 'IN'
        if len(items) == 1:
            items = items[0]
            operator = '='
        cur = Sqlite.cursor()
        query = f"""
                DELETE FROM Tasks
                WHERE id {operator} {items} OR label {operator} {items};
            """
        cur.executescript(query)
        cur.connection.commit()

    @classmethod
    def last_toggle_item(cls, _id: int, fields: list):
        query = f"""
                    SELECT {', '.join(fields)} FROM Times
                    WHERE task_id = {_id}
                    ORDER BY ID DESC LIMIT 1
                """
        return Sqlite.cursor().execute(query).fetchone()

    @classmethod
    def toggle(cls, _id: typing.Union[int, str]):
        fields = ['id', 'start', 'end']
        lti = cls.last_toggle_item(_id, fields)
        start_index = fields.index('start')
        end_index = fields.index('end')
        is_ended = lambda time_item, index=end_index: time_item[index]
        cursor = Sqlite.cursor()
        if not lti or is_ended(lti):
            query = f"""INSERT INTO Times (start, task_id)
                VALUES ('{str(datetime.now())}', {_id})"""
            cls.set_in_progress(_id, _cur=cursor)
        else:
            time_id = lti[0]
            query = f"""UPDATE Times
                    SET end = '{datetime.now()}'
                WHERE id = {time_id}"""
            cls.update_total_time(_id, datetime.fromisoformat(lti[start_index]), datetime.now(), _cur=cursor)
        try:
            print(query)
            cursor.execute(query)
            cursor.connection.commit()
        except sqlite3.IntegrityError:
            print('wrong id')
        return lti

    @classmethod
    def update_total_time(cls, _id, start: datetime, end: datetime, _cur: sqlite3.Cursor = None):
        cur = _cur or Sqlite.cursor()
        secs = int((end - start).total_seconds())
        cur.execute(
            f"""
                    UPDATE Tasks
                    SET total_time = total_time + {secs},
                        state = 'done'
                    WHERE id = {_id}
                """
        )
        if not _cur:
            cur.connection.commit()
        return secs

    @classmethod
    def set_in_progress(cls, _id: int, _cur: sqlite3.Cursor = None):
        cur = _cur or Sqlite.cursor()
        query = f"""UPDATE Tasks
                    SET state = 'in_progress'
                    WHERE id = {_id}"""
        cur.execute(query)
        if not _cur:
            cur.connection.commit()
