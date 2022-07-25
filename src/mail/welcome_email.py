from dataclasses import dataclass
from mail.email import Email
from mail.raw_email import RawEmail
from models.user import User


@dataclass
class WelcomeEmail(Email):
    def __init__(self, user: User) -> None:
        self.to = user.name
        self.subject = "Welcome to Emag price tracker"

    def format_mails(self) -> list[Email]:
        email_text = f"Welcome, {self.to}, to Emag price tracker - the app that lets you track product prices, sales and helps you make better purchases"
        return [RawEmail(self.to, self.subject, email_text)]
