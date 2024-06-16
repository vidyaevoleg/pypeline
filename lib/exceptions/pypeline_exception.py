from typing import Union, Optional


class PypelineException(Exception):
    """
    Base class for exceptions in the pypeline package.
    """
    inner_exception: Exception

    def __init__(self, reason: Union[str, Exception], info: Optional[str] = None):
        message = reason if isinstance(reason, str) else reason.__str__()
        if isinstance(reason, Exception):
            self.inner_exception = reason

        message = f"Error during pypeline execution: {message}"

        if info:
            message += f'{info}\n\n'

        super().__init__(message)
