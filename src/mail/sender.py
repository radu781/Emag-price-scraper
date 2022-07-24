import smtplib, ssl
from time import sleep

from mail.email import Email
from . import _from, _password


class EmailSender:
    FROM: str = _from
    PASSWORD: str = _password
    mails: list[Email] = []

    @staticmethod
    def queue(email: Email):
        email.message["From"] = EmailSender.FROM
        for mail in email.format_mails():
            EmailSender.mails.append(mail)
        EmailSender.__send()

    @staticmethod
    def __send_single(email: Email) -> None:
        print("Sending email", email.text)
        if EmailSender.FROM == "" or EmailSender.PASSWORD == "":
            return

        with smtplib.SMTP_SSL(
            "smtp.gmail.com", 465, context=ssl.create_default_context()
        ) as server:
            server.login(EmailSender.FROM, EmailSender.PASSWORD)
            server.sendmail(EmailSender.FROM, email.to, email.message.as_string())
            server.quit()

    @staticmethod
    def __send()->None:
        while EmailSender.mails != []:
            EmailSender.__send_single(EmailSender.mails.pop(0))
            sleep(1.5)
