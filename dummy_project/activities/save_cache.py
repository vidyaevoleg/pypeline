from typing import Any

from pydantic import BaseModel

from lib.activity import Activity


class SaveCacheInput(BaseModel):
    key: str
    data: dict


class SaveCache(Activity[SaveCacheInput, Any]):
    def call(self, **kwargs):
        print(f'Cache saved with key {self.input.key} and data {self.input.data}')