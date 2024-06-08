from dummy_project.models.user import User
from dummy_project.activities.create_user import CreateUserInput, CreateUser
from dummy_project.pipelines.create_user_pypeline import CreateUserPypeline

# EXAMPLE

input = {"email": "oleg@gmail.com", "first_name": "Oleg", "last_name": "Smith"}
current_user = User("1", "admin", "test@gmail.com")
pypeline = CreateUserPypeline(input, current_user=current_user)
result = pypeline()

if result.ok:
    print(f"Success")
else:
    print(f"Failed: {result.error}")
