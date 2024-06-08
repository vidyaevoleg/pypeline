from pydantic import BaseModel
from lib.activity import Activity

class NotifyAdminInput(BaseModel):
    message: str

class NotifyAdmin(Activity[NotifyAdminInput, None]):
    def call(self):
        print(f'Admin notified about: {self.input.message}')
