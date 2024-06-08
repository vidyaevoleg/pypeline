from typing import Optional, TypeVar,  Union, Generic
from lib.activity_error import ActivityError

TInput = TypeVar('TInput', bound=any)
TOutput = TypeVar('TOutput', bound=any)


class ActivityResult(Generic[TOutput]):
    ok: bool
    output: Optional[TOutput]
    errors: list[ActivityError]
    context: dict[str, any]

    def __init__(self, ok: bool,
                 output: Optional[any] = None,
                 error: Union[str, Exception] = None,
                 context: dict[str, any] = {},
                 **kwargs):
        self.ok = ok
        self.output = output
        self.context = context
        self.error = self.parse_error(error)

    @staticmethod
    def ok(output: TOutput, **kwargs) -> 'ActivityResult':
        return ActivityResult(True, output, **kwargs)

    @staticmethod
    def fail(reason: Union[str, Exception], **kwargs) -> 'ActivityResult':
        # if isinstance(reason, Exception):
        #     return ActivityResult(False, None, reason, **kwargs)

        return ActivityResult(False, None, reason, **kwargs)

    @staticmethod
    def parse_error(error: Union[str, Exception]) -> ActivityError:
        return ActivityError('exception', str(error))
