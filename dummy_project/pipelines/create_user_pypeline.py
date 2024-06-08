from dummy_project.activities.authorize import Authorize
from dummy_project.activities.create_profile import CreateProfile
from dummy_project.activities.create_user import CreateUserInput, CreateUser
from dummy_project.activities.notify_admin import NotifyAdmin
from dummy_project.activities.send_email import SendEmail
from dummy_project.models.user import User
from lib.pypeline import Pypeline


class CreateUserPypeline(Pypeline[CreateUserInput, User]):

    def call(self):
        self.step(Authorize, input=self.authorize_input)
        self.step(CreateUser, output=self.create_user_output)
        self.step(CreateProfile, input=self.create_profile_input)
        self.step(SendEmail, input=self.send_email_input)
        self.fail(NotifyAdmin, input=self.notify_admin_input)
        self.step(self.return_user)

    def authorize_input(self, current_user: User, **ctx):
        return {
            "user_id": current_user.id,
            "permission": "invite"
        }, ctx

    def create_user_output(self, output: User, **ctx):
        ctx['user'] = output  # cache user in the context
        return output, ctx

    def create_profile_input(self, user: User, **ctx):
        return {
            "user_id": user.id,
            "email": user.email
        }, ctx

    def send_email_input(self, user: User, current_user: User, **ctx):
        return {
            "to": user.email,
            "subject": "Welcome",
            "from": current_user.email,
            "body": f"Welcome {user.first_name}. You're invited by {current_user.email}"
        }, ctx

    def notify_admin_input(self, **ctx):
        return {
            "message": f"Failed to create user with email {self.input.email}"
        }, ctx

    def return_user(self, user: User, **ctx):
        return user, ctx