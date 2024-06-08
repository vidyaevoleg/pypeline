from typing import Type, Optional, TypeVar, Callable, Union

TInput = TypeVar('TInput', bound=any)
TOutput = TypeVar('TOutput', bound=any)


class ActivityError:
    code: str
    message: str

    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
