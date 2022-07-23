import asyncio
from dataclasses import dataclass, field
import hashlib
from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString
from models.item import Item
from scraper.scraper import ElementNotFoundException, Scraper
import aiohttp
import requests


@dataclass
class EmagScraper(Scraper):
    PAGE_LIMIT: int = field(init=False, default=10000)

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

    async def get_results(self) -> list[Item]:
        async with aiohttp.ClientSession() as session:
            tasks: list[asyncio.Future[list[Item]]] = []
            for page_index in range(2, min(self.pages + 2, EmagScraper.PAGE_LIMIT)):
                try:
                    tasks.append(
                        asyncio.ensure_future(
                            self._get_details(
                                session, self.current_link + f"/p{page_index}"
                            )
                        )
                    )
                except:
                    break
            result = await asyncio.gather(*tasks)
            out: list[Item] = []
            for row in result:
                for item in row:
                    out.append(item)
            return out

    async def _get_details(
        self, session: aiohttp.ClientSession, url: str
    ) -> list[Item]:
        out: list[Item] = []

        try:
            async with session.get(url) as response:
                cards = BeautifulSoup(await response.text(), "html.parser").find_all(
                    class_="card-v2"
                )
                for card in cards:
                    try:
                        link = self._get_link(card)
                        out.append(
                            Item(
                                self._get_title(card),
                                link,
                                self._get_price(card),
                                self._get_image(card),
                                hashlib.sha256(bytes(link, "utf-8")).hexdigest()[:16]
                            )
                        )
                    except ElementNotFoundException:
                        pass
        except:
            return []
        return out

    def _get_title(self, soup: BeautifulSoup) -> str:
        title = soup.find(class_="card-v2-title")

        if title is None:
            raise ElementNotFoundException()
        return title.text.strip()

    def _get_image(self, soup: BeautifulSoup) -> str:
        image_div = soup.find(class_="card-v2-thumb")

        if image_div is None or isinstance(image_div, NavigableString):
            return "resources/images/not_found.jpg"
        img = image_div.contents[0]
        if not isinstance(img, Tag):
            return "resources/images/not_found.jpg"

        try:
            return self.get_raw_link(str(img["src"]))
        except KeyError:
            raise ElementNotFoundException()

    def _get_price(self, soup: BeautifulSoup) -> str:
        price = soup.find(class_="product-new-price")

        if price is None:
            raise ElementNotFoundException()
        return price.text.strip()

    def _get_link(self, soup: BeautifulSoup) -> str:
        link = soup.find(class_="card-v2-thumb")

        if link is None or isinstance(link, NavigableString):
            raise ElementNotFoundException()
        return self.get_raw_link(str(link["href"]))
