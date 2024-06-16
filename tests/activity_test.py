from pydantic import BaseModel
from lib.activity import Activity


class DummyActivityInput(BaseModel):
    message: str


class DummyActivity(Activity[DummyActivityInput, str]):
    def call(self) -> str:
        return self.input.message


def test_success_with_dict_input():
    activity = DummyActivity({"message": "Hello World"})
    result = activity()
    assert result.ok
    assert result.output == "Hello World"


def test_success_with_pydantic_input():
    activity = DummyActivity(DummyActivityInput(message="Hello World"))
    result = activity()
    assert result.ok
    assert result.output == "Hello World"


def test_fail_with_invalid_input():
    activity = DummyActivity({"invalid": "Hello World"})
    result = activity()
    assert not result.ok
    # TODO check for specific message
    assert result.error is not None
