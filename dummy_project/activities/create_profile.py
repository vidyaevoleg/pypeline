from pydantic import BaseModel

from dummy_project.models.profile import Profile
from lib.activity import Activity


class CreateProfileInput(BaseModel):
    user_id: str
    email: str


class CreateProfile(Activity[CreateProfileInput, Profile]):
    def call(self):
        if self.input.email == '':
            raise Exception('Email is required')

        if self.input.user_id == '':
            raise Exception('User ID is required')

        profile = Profile(self.input.user_id, self.input.email)

        try:
            profile.save()
            return profile
        except Exception as _e:
            raise Exception('Error saving profile to the database')
