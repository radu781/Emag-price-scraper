from dataclasses import dataclass, field
from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString
from scraper.scraper import Scraper
import requests


@dataclass
class EmagScraper(Scraper):
    all_soup: BeautifulSoup = field(init=False)
    one_page_soup: BeautifulSoup = field(init=False)
    links: list[str] = field(init=False)
    search_results: list[str] = field(init=False, default_factory=list[str])

    def __post_init__(self) -> None:
        self.current_link = self.BASE_LINK + self.user_prompt
        page = requests.get(self.current_link)
        self.all_soup = BeautifulSoup(page.content, "html.parser")

    def get_results(self) -> list[dict[str, str]]:
        individual_results = self.all_soup.find_all(class_="card-item")
        out: list[dict[str, str]] = []

        for result in individual_results:
            if self.search_count <= 0:
                break
            out.append(self._get_details(result))
            self.search_count -= 1

        return out

    def _get_details(self, soup: BeautifulSoup) -> dict[str, str]:
        return {
            "title": self._get_title(soup),
            "link": self._get_link(soup),
            "price": self._get_price(soup),
            "image": self._get_image(soup),
        }

    def _get_title(self, soup: BeautifulSoup) -> str:
        title = soup.find(class_="card-v2-title")

        if title is None:
            return "N/A"
        return title.text.strip()

    def _get_image(self, soup: BeautifulSoup) -> str:
        image_div = soup.find(class_="card-v2-thumb")

        if image_div is None or isinstance(image_div, NavigableString):
            return "resources/images/not_found.jpg"
        return image_div.img["src"]  # type: ignore

    def _get_price(self, soup: BeautifulSoup) -> str:
        price = soup.find(class_="product-new-price")

        if price is None:
            return "-1"
        return price.text.strip()

    def _get_link(self, soup: BeautifulSoup) -> str:
        link = soup.find(class_="card-v2-thumb")

        if link is None or isinstance(link, NavigableString):
            return "Link not found"
        return str(link["href"])
