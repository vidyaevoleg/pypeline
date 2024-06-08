from pydantic import BaseModel

from dummy_project.models.user import User
from lib.activity import Activity


class CreateUserInput(BaseModel):
    email: str
    first_name: str
    last_name: str


class CreateUser(Activity[CreateUserInput, User]):
    def call(self):
        if self.input.email == '':
            raise Exception('Email is required')
        if self.input.first_name == '':
            raise Exception('First name is required')
        if self.input.last_name == '':
            raise Exception('Last name is required')

        if User.exists(self.input.email):
            raise Exception('Email already exists')

        user = User(self.input.first_name, self.input.last_name, self.input.email)
        try:
            user.save()
            return user
        except Exception as _e:
            raise Exception('Error saving user to the database')
