from mail.email import Email


class RawEmail(Email):
    def format_mails(self) -> list[Email]:
        return super().format_mails()
