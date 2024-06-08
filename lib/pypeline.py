import traceback
from typing import TypeVar, Callable, Type
from pydantic import ValidationError
from .activity import Activity

TInput = TypeVar('TInput', bound=any)
TOutput = TypeVar('TOutput', bound=any)
TPypelineActivity = Type[Activity] | Callable[[any], any]


class Pypeline(Activity[TInput, TOutput]):
    def __init__(self, input: TInput, **kwargs):
        super().__init__(input, **kwargs)

    def step(self,
            activity: TPypelineActivity,
            input: Callable[[any], any] = None,
            output: Callable[[any], any] = None):

        # skipping the next steps if the pypeline is already failed
        if self._ok:
            self._run_activity(activity, input, output)

    def fail(self,
             activity: TPypelineActivity,
             input: Callable[[any], any] = None,
             output: Callable[[any], any] = None):

        # running fail steps only if the pypeline is already failed
        if not self._ok:
            self._run_activity(activity, input, output)

    def _run_activity(self,
                      activity: TPypelineActivity,
                      input: Callable[[any], any] = None,
                      output: Callable[[any], any] = None,
                      **kwargs):
        # check that activity is pure function
        activity_context = {**self.ctx, **kwargs}
        activity_input = self.input

        # if custom input is provided
        if input:
            try:
                activity_input, activity_context = self.__build_input(input, **activity_context)
            except Exception as exception:
                self._fail(exception, info=f'Error processing input: {exception} for activity {activity.__name__}')
                return

        if callable(activity):
            activity_instance = Activity(activity_input, callback=activity, **activity_context)
        else:
            activity_instance = activity(activity_input, **activity_context)

        activity_result = activity_instance(**activity_context)

        if not activity_result.ok:
            self._fail(activity_result)
            return

        if activity_result.ok:
            activity_output, activity_context = self.__build_output(activity_result, output, **activity_context)
            self._succeed(activity_output)
            self.ctx = {**self.ctx, **activity_context}
        else:
            self._fail(activity_result)

    def __build_input(self, input, **ctx) -> [any, dict]:
        custom_input, custom_context = input(**ctx)
        return custom_input, {**ctx, **custom_context}

    def __build_output(self, activity_result, output: Callable[[any], any] = None, **ctx) -> [any, dict]:
        if output:
            activity_output, activity_context = output(activity_result.output, **ctx)
        else:
            activity_output = activity_result.output
            activity_context = ctx

        return activity_output, activity_context
