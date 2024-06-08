The project is inspired by [Trailblazer](https://trailblazer.to/) from Ruby world.

The idea is to have declarative way to define business logic in a way that is easy to understand and maintain.

Dependencies:
- [Pydantic](https://docs.pydantic.dev/latest/) for data validation

Example syntax:
```python
from pydantic import BaseModel

class CreateUserInput(BaseModel):
    email: str
    first_name: str
    last_name: str

class CreateUserPypeline(Pypeline[CreateUserInput, User]):

    def call(self):
        self.run(Authorize, input=self.authorize_input)
        self.run(CreateUser, output=self.create_user_output)
        self.run(SendEmail, input=self.send_email_input)
        self.fail(NotifyAdmin, input=self.notify_admin_input)

    def authorize_input(self, current_user: User, **ctx):
        return {
            "user_id": current_user.id,
            "permission": "invite"
        }

    def create_user_output(self, output: User, **ctx):
        ctx['user'] = output  # cache user in the context
        return output, ctx

    def create_profile_input(self, user: User, **ctx):
        return {
            "user_id": user.id,
            "email": user.email
        }

    def send_email_input(self, user: User, **ctx):
        return {
            "to": user.email,
            "subject": "Welcome",
            "body": f"Welcome {user.first_name}"
        }

    def notify_admin_input(self, user: User, **ctx):
        return user


# Usage
input = {"email": "oleg@gmail.com",  "first_name": "Oleg", "last_name": "Smith")
current_user = User()
pypeline = CreateUserPypeline(input, current_user=current_user)
```