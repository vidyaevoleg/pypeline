from typing import Any

from pydantic import BaseModel

from lib.activity import Activity


class AddToBlacklistInput(BaseModel):
    email: str


class AddToBlacklist(Activity[AddToBlacklistInput, Any]):
    def call(self):
        print(f'Email {self.input.email} added to blacklist')
