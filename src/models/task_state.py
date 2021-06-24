from enum import Enum


class TaskState(str, Enum):
    DONE = 'done'
    IN_PROGRESS = 'in_progress'
    TODO = 'todo'
