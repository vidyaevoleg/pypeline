from typing import Optional, Tuple, Any, Dict
from lib.activity import Activity
from lib.exceptions.pypeline_exception import PypelineException
from lib.types import TPypelineActivity, TPypelineFunc


class PypelineActivity(Activity[None, None]):
    """
        PypelineActivity is a class that wraps the Activity class within a pypeline.
        Basically, it contains 3 important steps:
         - process the input via the input function
         - call the activity with the input
         - process the output via the output function

    """
    _activity: TPypelineActivity
    _initial_input: Optional[Any]
    _input_callback: Optional[TPypelineFunc]
    _output_callback: Optional[TPypelineFunc]

    def __init__(self,
                 activity: TPypelineActivity,
                 input: Optional[Any] = None,
                 input_callback: Optional[TPypelineFunc] = None,
                 output_callback: [TPypelineFunc] = None,
                 **kwargs):

        self._initial_input = input
        self._input_callback = input_callback
        self._output_callback = output_callback
        self._activity = activity
        self._ctx = kwargs
        # initialize a dummy activity class with empty input and output
        # mostly just to reuse the Activity class features (eg. error handling, context management, etc.)
        super().__init__(**self._ctx)

    def call(self):
        # STEP 1: process the input
        activity_input, activity_context = self._build_input()

        # STEP 2: run the activity
        activity_result = self._build_activity(activity_input, **activity_context)()

        # STEP 3: process the output
        activity_output, activity_context = self._build_output(activity_result, **activity_context)

        self._ctx = activity_context
        self._output = activity_output

        return self._output

    def _build_input(self, **kwargs) -> Optional[Tuple[Any, Dict]]:
        ctx = {**self._ctx, **kwargs}

        if self._input_callback:
            try:
                result = self._input_callback(**ctx)
            except Exception as exception:
                raise PypelineException(exception, info=f'Error processing during input')

            if isinstance(result, tuple):
                activity_input, activity_context = result
            else:
                activity_input, activity_context = result, ctx

            return activity_input, {**ctx, **activity_context}
        else:
            return self._initial_input, ctx

    def _build_output(self, activity_result, **kwargs) -> Optional[Tuple[Any, Dict]]:
        ctx = {**self._ctx, **kwargs}

        if self._output_callback:
            try:
                result = self._output_callback(activity_result.output, **ctx)
            except Exception as exception:
                raise PypelineException(exception, info=f'Error during processing output')

            if isinstance(result, tuple):
                custom_output, custom_context = result
            else:
                custom_output, custom_context = result, ctx
            return custom_output, {**ctx, **custom_context}

        else:
            return activity_result.output, ctx

    def _build_activity(self, activity_input: Optional[Any], **kwargs) -> Activity:
        ctx = {**self._ctx, **kwargs}

        try:
            if isinstance(self._activity, type) and issubclass(self._activity, Activity):
                # activity is an Activity child
                return self._activity(activity_input, **ctx)
            elif callable(self._activity):
                # activity is a function
                return Activity(activity_input, callback=self._activity, **ctx)
        except Exception as exception:
            raise PypelineException(exception, info=f'Error during instantiating an activity')

        # not enable to recognize the activity
        raise PypelineException(f'Not able to run activity {self._activity.__name__}: must be a function or '
                                f'inherited from Activity')
