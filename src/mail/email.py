from dataclasses import dataclass, field
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


@dataclass
class Email:
    to: str
    subject: str
    text: str
    html: str = field(default="")
    message: MIMEMultipart = field(init=False, default=MIMEMultipart("alternative"))

    def __post_init__(self) -> None:
        self.message["Subject"] = self.subject
        self.message["To"] = self.to

        self.message.attach(MIMEText(self.text, "plain"))
        if self.html != "":
            self.message.attach(MIMEText(self.html, "html"))
