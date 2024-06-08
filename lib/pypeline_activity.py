from abc import ABC
from typing import Callable, Type
from lib.activity import Activity


class PypelineActivity(ABC):
    process_input: Callable[[any], any]
    process_output: Callable[[any], any]
    process_skip: Callable[[any], bool]


