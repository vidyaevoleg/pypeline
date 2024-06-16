from typing import Optional, TypeVar, Union, Generic, Any, Dict
from lib.activity_error import ActivityError

TInput = TypeVar('TInput', bound=Any)
TOutput = TypeVar('TOutput', bound=Any)
TCtx = Dict[str, Any]


class ActivityResult(Generic[TOutput]):
    ok: bool
    output: Optional[TOutput]
    errors: list[ActivityError]
    ctx: TCtx

    def __init__(self, ok: bool,
                 output: Optional[Any] = None,
                 error: Union[str, Exception] = None,
                 **kwargs):
        self.ok = ok
        self.output = output
        self.error = self.parse_error(error)
        self.ctx = kwargs

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
