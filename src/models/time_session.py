from . import BaseModel, datetime, typing, timedelta


class Timer(BaseModel):
    start: datetime
    end: typing.Optional[datetime]

    @property
    def duration(self) -> timedelta:
        return (self.end or datetime.now()) - self.start

    @property
    def seconds(self):
        return int(self.duration.total_seconds())
