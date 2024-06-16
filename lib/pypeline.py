from typing import TypeVar,  Optional, Any, List
from .activity import Activity
from .pypeline_activity import PypelineActivity, TPypelineActivity, TPypelineFunc

TInput = TypeVar('TInput', bound=Any)
TOutput = TypeVar('TOutput', bound=Any)


class Pypeline(Activity[TInput, TOutput]):
    _activities: List[PypelineActivity] = []

    def __call__(self, **kwargs):
        super().__call__(**kwargs)

        # to return the last activity output
        return self._activities[-1].result if self._activities else None

    def step(self,
             activity: TPypelineActivity,
             input: Optional[TPypelineFunc] = None,
             output: Optional[TPypelineFunc] = None):

        # skipping the next steps if the pypeline is already failed
        if self._ok:
            pypeline_activity = PypelineActivity(activity, self.input, input_callback=input, output_callback=output, **self.ctx)
            self._run_activity(pypeline_activity)

    def fail(self,
             activity: TPypelineActivity,
             input: Optional[TPypelineFunc] = None,
             output: Optional[TPypelineFunc] = None):

        # running fail steps only if the pypeline is already failed
        if not self._ok:
            pypeline_activity = PypelineActivity(activity, self.input, input_callback=input, output_callback=output, **self.ctx)
            self._run_activity(pypeline_activity)

    def _run_activity(self, activity: PypelineActivity, **kwargs):
        activity_result = activity(**kwargs)

        self._activities.append(activity)

        if activity_result.ok:
            self._succeed(activity_result)
        else:
            self._fail(activity_result)