from pydantic import BaseModel
from lib.activity import Activity
from lib.pypeline import Pypeline


class DummyInput(BaseModel):
    message: str


class DownCaseActivity(Activity[DummyInput, str]):
    def call(self):
        return self.input.message.lower()


class DummyPypeline(Pypeline[DummyInput, str]):
    def call(self, **ctx):
        self.step(DownCaseActivity, output=self.down_case_output)
        self.step(self.remove_world, input=self.remove_world_input)

    def down_case_output(self, output: str, **ctx):
        ctx['word'] = output
        return output, ctx

    def remove_world_input(self, word: str) -> str:
        return word

    def remove_world(self, word: str) -> str:
        # remove spaces and "World" from the word
        return word.replace("world", "").strip()


def test_success_with_dict_input():
    pypeline = DummyPypeline({"message": "Hello World"})
    result = pypeline()
    assert result.ok == True
    assert result.output == "hello"
