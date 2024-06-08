from dummy_project.models.user import User


class Profile:
    def __init__(self, user_id: str, email: str):
        self.user_id = user_id
        self.email = email

    def save(self):
        pass
