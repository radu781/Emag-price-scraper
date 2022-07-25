from dataclasses import dataclass
from mail.email import Email
from mail.raw_email import RawEmail
from utils.database.user_dao import UserDAO


@dataclass
class PriceEmail(Email):
    def __init__(self, obj: list[dict[str, str | list[str] | float]]) -> None:
        self.raw = obj
        self.subject = "Product price update"

    def format_mails(self) -> list[Email]:
        pairs: dict[str, list[str]] = {}
        for item in self.raw:
            for user_id in item["users"]:
                current_email = UserDAO.get_user(user_id).name
                if not current_email in pairs:
                    pairs[current_email] = []
                pairs[current_email].append(item["itemId"])

        emails: list[Email] = []
        for user_email in pairs:
            changed = ", ".join(item_id for item_id in pairs[user_email])
            current_text = f"Hello, {user_email}!\nItems with id [{changed}] have changed price"
            emails.append(RawEmail(user_email, self.subject, current_text))

        return emails
