from dummy_project.models.user import User
from dummy_project.pipelines.create_user_pypeline import CreateUserPypeline


current_user = User("1", "admin", "test@gmail.com")
input = {"email": "james@smith.com", "first_name": "James", "last_name": "Smith"}
pypeline = CreateUserPypeline(input, current_user=current_user)
result = pypeline()

if result.ok:
    print(f"Success")
else:
    print(f"Failed: {result.error}")
