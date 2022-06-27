from dataclasses import dataclass, field
from bs4 import BeautifulSoup
from bs4.element import Tag
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

    def get_results(self) -> list[str]:
        individual_results = self.all_soup.find_all(class_="card-v2-info")

        for result in individual_results:
            current_product = BeautifulSoup(bytes(str(result), "utf-8"), "html.parser")
            product_link = current_product.find(class_="card-v2-thumb")

            if not isinstance(product_link, Tag):
                continue
            self.search_results.append(str(product_link["href"]))

        return self.search_results

    def get_details(self, link: str) -> dict[str, str]:
        html = requests.get(link)
        current_soup = BeautifulSoup(html.content, "html.parser")
        return {
            "title": self._get_title(current_soup),
            "link": link,
            "price": self._get_price(current_soup),
            "image": self._get_image(current_soup),
        }

    def _get_title(self, soup: BeautifulSoup) -> str:
        title = soup.find(class_="page-title")

        if title is not None:
            return title.text.strip()
        return ""

    def _get_image(self, soup: BeautifulSoup) -> str:
        return super()._get_image(soup)

    def _get_price(self, soup: BeautifulSoup) -> str:
        price = soup.find(class_="product-new-price")

        if price is not None:
            return price.text.strip()
        return ""
