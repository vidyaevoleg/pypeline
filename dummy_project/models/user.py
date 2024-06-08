
class User:
    def __init__(self, first_name: str, last_name: str, email: str):
        self.id = email
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def save(self):
        pass

    @staticmethod
    def exists(_email: str):
        return False
