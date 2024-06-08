from typing import Any

from pydantic import BaseModel

from lib.activity import Activity


class SendEmailInput(BaseModel):
    to: str
    subject: str
    body: str


class SendEmail(Activity[SendEmailInput, Any]):
    def call(self):
        print(f'Email sent to {self.input.to} with subject {self.input.subject} and body {self.input.body}')
