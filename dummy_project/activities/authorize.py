from pydantic import BaseModel

from dummy_project.models.user import User
from lib.activity import Activity


class AuthorizeInput(BaseModel):
    user_id: str
    permission: str


class Authorize(Activity[AuthorizeInput, None]):
    def call(self, current_user: User, **kwargs):
        print(f"Authorize called for user {current_user.id} with permission {self.input.permission}")