from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any


@dataclass
class Email(ABC):
    to: str
    subject: str
    raw: Any = field(init=False)
    text: str = field(default="")
    html: str = field(default="")
    message: MIMEMultipart = field(init=False, default=MIMEMultipart("alternative"))

    def __post_init__(self) -> None:
        self.message["Subject"] = self.subject
        self.message["To"] = self.to

        self.message.attach(MIMEText(self.text, "plain"))
        if self.html != "":
            self.message.attach(MIMEText(self.html, "html"))

    @abstractmethod
    def format_mails(self) -> list[Email]:
        ...
