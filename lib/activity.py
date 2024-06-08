import inspect
import traceback
from typing import Optional, TypeVar, Generic, Dict, Any, Union, Type, overload, Callable

from pydantic import BaseModel, ValidationError

from lib.activity_result import ActivityResult

TInput = TypeVar('TInput', bound=Union[BaseModel, dict])
TOutput = TypeVar('TOutput')


class Activity(Generic[TInput, TOutput]):
    input: TInput
    ctx: Dict[str, Any] = {}
    result: ActivityResult

    _id: str = None
    _ok: bool = True
    _error: Optional[Exception] = None
    _output: Optional[TOutput] = None
    _callback: Optional[Callable[[any], any]] = None

    def __init__(self, input, callback: Optional[Callable[[any], any]] = None, **kwargs):
        self.ctx = kwargs
        self.input = input
        self._callback = callback
        self._id = callback.__name__ if callback else self.__class__.__name__

    def __call__(self, **ctx) -> 'ActivityResult':
        activity_name = self.__class__.__name__
        activity_context = {**self.ctx, **ctx}

        print(f'Running activity: {activity_name}')

        try:
            self.input = self.__build_input()
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
            return ActivityResult.ok(self._output, **self.ctx)
        else:
            return ActivityResult.fail(self._error, **self.ctx)

    @property
    def output(self) -> Optional[TOutput]:
        return self._output

    def __build_input(self) -> BaseModel:
        # Getting the first type argument assuming that it's a pydantic class
        try:
            expected_input_type = self.__orig_bases__[0].__args__[0]
        except Exception as _e:
            raise ValueError('Generic input type was not provided')

        if issubclass(expected_input_type, BaseModel):
            if isinstance(self.input, dict):
                # an exception is usually thrown hee if the input is not valid
                return expected_input_type(**self.input)
            elif isinstance(self.input, BaseModel):
                return self.input
            else:
                raise ValueError('Input must be a dict or a pydantic model')
        else:
            # TODO replace with issubclass
            if self.input.__class__ == expected_input_type:
                return self.input
            else:
                raise ValueError(f'Input must be of type {expected_input_type.__name__}')

    def _fail(self, reason: Union[ActivityResult, Exception], info: Optional[str] = None):
        self._ok = False
        self._output = None

        if info:
            print(info)

        if isinstance(reason, ActivityResult):
            self._error = reason.error
        else:
            error = traceback.format_exc(reason)
            print(error)
            self._error = reason

    def _succeed(self, output: Union[ActivityResult, TOutput]):
        self._ok = True
        self._error = None
        if isinstance(output, ActivityResult):
            self._output = output.output
        else:
            self._output = output
