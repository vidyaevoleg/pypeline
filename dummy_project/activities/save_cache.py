from pydantic import BaseModel

from lib.activity import Activity


class SaveCacheInput(BaseModel):
    key: str
    data: dict


class SaveCache(Activity[SaveCacheInput, any]):
    def call(self, **kwargs) -> any:
        print(f'Cache saved with key {self.input.key} and data {self.input.data}')