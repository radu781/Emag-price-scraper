from cmath import sqrt
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
        footer: list[Tag] = self.all_soup.find_all(class_="listing-panel")
        results = footer[1].find(class_="listing-panel-footer")
        if not isinstance(results, Tag):
            self.pages = 1
            return
        numbers: list[Tag] = results.find_all(class_="js-change-page")
        self.pages = int(numbers[-2].text.strip())

    def get_results(self) -> list[dict[str, str]]:
        out: list[dict[str, str]] = []
        for page_index in range(2, int(sqrt(self.pages + 1).real)):
            current_page = requests.get(self.current_link + f"/p{page_index}")
            current_soup = BeautifulSoup(current_page.content, "html.parser")

            individual_results = current_soup.find_all(class_="card-item")

            for result in individual_results:
                out.append(self._get_details(result))

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
        img = image_div.contents[0]
        if not isinstance(img, Tag):
            return "resources/images/not_found.jpg"

        try:
            return str(img["src"])
        except KeyError:
            print(img)
            return "resources/images/not_found.jpg"

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
