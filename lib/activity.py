import inspect
import traceback
from typing import Optional, TypeVar, Generic, Dict, Any, Union, overload, Callable
from pydantic import BaseModel
from lib.activity_error import ActivityError
from lib.activity_result import ActivityResult

TInput = TypeVar('TInput', bound=Union[BaseModel, dict])
TOutput = TypeVar('TOutput', bound=Any)
TCtx = Dict[str, Any]


class Activity(Generic[TInput, TOutput]):
    input: TInput

    _id: str = None
    _ok: bool = True
    _ctx: TCtx = {}
    _error: Optional[Exception] = None
    _output: Optional[TOutput] = None
    _callback: Optional[Callable[[Any], Any]] = None
    _expected_input_type: Optional[type] = None

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if hasattr(cls, '__orig_bases__'):
            for base in cls.__orig_bases__:
                if hasattr(base, '__args__') and base.__args__:
                    cls._expected_input_type = base.__args__[0]
                    break

    def __init__(self, input: Optional[Any] = None, callback: Optional[Callable[[Any], Any]] = None, **kwargs):
        self.input = input
        self._ctx = kwargs
        self._callback = callback
        self._id = callback.__name__ if callback else self.__class__.__name__

    def __call__(self, **ctx) -> 'ActivityResult':
        activity_name = self.__class__.__name__
        activity_context = {**self._ctx, **ctx}

        print(f'Running activity: {activity_name}')

        try:
            self.input = self.__coerce_input()
            method = self._callback if self._callback else getattr(self, 'call')
            if len(inspect.signature(method).parameters) > 0:
                # The call method accepts keyword arguments
                result = method(**activity_context)
            else:
                # The call method does not accept any arguments
                result = method()
            self._succeed(result)
        except Exception as exception:
            self._fail(exception)

        return self.result

    @overload
    def call(self) -> TOutput:
        ...

    @overload
    def call(self, **kwargs) -> TOutput:
        ...

    def call(self, **kwargs) -> TOutput:
        raise NotImplementedError('Activity call method must be implemented')

    @property
    def result(self) -> ActivityResult[TOutput]:
        if self._ok:
            return ActivityResult.ok(self._output, **self._ctx)
        else:
            return ActivityResult.fail(self._error, **self._ctx)

    @property
    def output(self) -> Optional[TOutput]:
        return self._output

    @property
    def ctx(self) -> TCtx:
        return self._ctx

    def __coerce_input(self) -> Optional[BaseModel]:
        # Getting the first type argument assuming that it's a pydantic class
        if self._expected_input_type is None:
            return

        if issubclass(self._expected_input_type, BaseModel):
            if isinstance(self.input, dict):
                # an exception is usually thrown hee if the input is not valid
                return self._expected_input_type(**self.input)
            elif isinstance(self.input, BaseModel):
                return self.input
            else:
                raise ValueError('Input must be a dict or a pydantic model')
        else:
            # TODO replace with issubclass
            if self.input.__class__ == self._expected_input_type:
                return self.input
            else:
                raise ValueError(f'Input must be of type {self._expected_input_type.__name__}')

    def _fail(self, reason: Union[ActivityResult, Exception, str], info: Optional[str] = None):
        self._ok = False
        self._output = None

        if info:
            print(info)

        if isinstance(reason, ActivityResult):
            self._error = reason.error
        elif isinstance(reason, str):
            self._error = ActivityError('base', reason)
        elif isinstance(reason, Exception):
            print(traceback.format_exc())
            self._error = reason

    def _succeed(self, output: Union[ActivityResult, TOutput]):
        self._ok = True
        self._error = None
        if isinstance(output, ActivityResult):
            self._output = output.output
            self._ctx = {**self._ctx, **output.ctx}
        else:
            self._output = output

