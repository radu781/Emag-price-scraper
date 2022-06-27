from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from bs4 import BeautifulSoup


@dataclass
class Scraper(ABC):
    BASE_LINK: str
    user_prompt: str
    current_link: str = field(init=False)

    @abstractmethod
    def get_results(self) -> list[str]:
        ...

    @abstractmethod
    def get_details(self, link: str) -> dict[str, str]:
        ...

    @abstractmethod
    def _get_title(self, soup: BeautifulSoup) -> str:
        ...

    @abstractmethod
    def _get_image(self, soup: BeautifulSoup) -> str:
        ...

    @abstractmethod
    def _get_price(self, soup: BeautifulSoup) -> str:
        ...
