from typing import Dict, Callable, Type, Any
from lib.activity import Activity

TPypelineFunc = Callable[[...], Any]
TPypelineActivity = Type[Activity] | TPypelineFunc
