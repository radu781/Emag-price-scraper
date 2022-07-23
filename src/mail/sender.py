import smtplib, ssl

from mail.email import Email
from . import _from, _password


class EmailSender:
    FROM: str = _from
    PASSWORD: str = _password
    mails: list[Email] = []

    @staticmethod
    def queue(email: Email):
        email.message["From"] = EmailSender.FROM
        EmailSender.mails.append(email)
        current_mail = EmailSender.mails[0]
        EmailSender.mails.remove(current_mail)
        EmailSender.__send(current_mail)

    @staticmethod
    def __send(email: Email) -> None:
        if EmailSender.FROM == "" or EmailSender.PASSWORD == "":
            return

        with smtplib.SMTP_SSL(
            "smtp.gmail.com", 465, context=ssl.create_default_context()
        ) as server:
            server.login(EmailSender.FROM, EmailSender.PASSWORD)
            server.sendmail(EmailSender.FROM, email.to, email.message.as_string())
            server.quit()
