from dataclasses import dataclass, field
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from . import _from, _password


@dataclass
class EmailSender:
    FROM: str = field(init=False, default=_from)
    PASSWORD: str = field(init=False, default=_password)
    to: str
    subject: str
    text: str
    html: str = field(default="")
    message: MIMEMultipart = field(init=False, default=MIMEMultipart("alternative"))

    def __post_init__(self) -> None:
        self.message["Subject"] = self.subject
        self.message["From"] = self.FROM
        self.message["To"] = self.to

        self.message.attach(MIMEText(self.text, "plain"))
        if self.html != "":
            self.message.attach(MIMEText(self.html, "html"))

    def send(self) -> None:
        if self.FROM == "" or self.PASSWORD == "":
            return

        with smtplib.SMTP_SSL(
            "smtp.gmail.com", 465, context=ssl.create_default_context()
        ) as server:
            server.login(self.FROM, self.PASSWORD)
            server.sendmail(self.FROM, self.to, self.message.as_string())
            server.quit()
