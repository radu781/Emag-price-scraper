import asyncio
from dataclasses import dataclass, field
from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString
from scraper.scraper import Scraper
import aiohttp
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
        if numbers == []:
            self.pages = 1
        else:
            self.pages = int(numbers[-2].text.strip())

    async def get_results(self) -> list[dict[str, str]]:
        async with aiohttp.ClientSession() as session:
            tasks = []
            for page_index in range(2, (self.pages + 2)//30):
                tasks.append(asyncio.ensure_future(self._get_details(session, self.current_link + f"/p{page_index}")))
            result = await asyncio.gather(*tasks)
            out:list[dict[str,str]]=[]
            for row in result:
                for item in row:
                    out.append(item)
            return out

    async def _get_details(self,session:aiohttp.ClientSession, url: str) -> list[dict[str, str]]:
        out:list[dict[str,str]] = []

        async with session.get(url) as response:
            cards = BeautifulSoup(await response.text(), "html.parser").find_all(class_="card-v2")
            for card in cards:
                out.append({
                    "title": self._get_title(card),
                    "link": self._get_link(card),
                    "price": self._get_price(card),
                    "image": self._get_image(card),
                })

        return out

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
