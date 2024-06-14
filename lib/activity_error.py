from typing import TypeVar, Any

TInput = TypeVar('TInput', bound=Any)
TOutput = TypeVar('TOutput', bound=Any)


class ActivityError(Exception):
    key: str
    message: str

    def __init__(self, key: str, message: str):
        self.key = key
        self.message = message
