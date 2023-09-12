from enum import Enum


class TaskStatus(Enum):
    ACTIVE = 1
    COMPLETED = 2
    DRAFT = 3
    DELETED = 4
