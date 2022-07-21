import asyncio
from datetime import datetime
from aioflask import session
from flask import Blueprint, request, jsonify
from flask.wrappers import Response

from controllers import _get_current_user
from scraper.emag_scraper import EmagScraper
from models.item import Item
from utils.argument_parser import *
from utils.database.item_dao import ItemDAO
from models.user import User

search_api = Blueprint("search_api", __name__)


@search_api.route("/api/search", methods=["GET"])
async def search() -> Response:
    session["last_page"] = request.url
    parser = ArgumentParser(
        request,
        {
            Argument("q", ArgType.Optional, None),
            Argument("search-count", ArgType.Optional, 50),
            Argument("price-min", ArgType.Optional, 0),
            Argument("price-max", ArgType.Optional, 10_000),
            Argument("refresh-items", ArgType.Optional, "off"),
        },
    )

    current_user = _get_current_user(session)
    current_user.status = User.Status.from_value(session.get("user_status", 3))
    values = parser.get_values()
    if values["q"] is None:
        return jsonify()

    if values["refresh-items"] == "on" and current_user.can_refresh:
        results = await _scrape_items(values)
        results = ItemDAO.add_tracking(results, current_user)
        current_date = datetime.now()
        ItemDAO.insert_multiple(results, current_date)
    else:
        results = _database_items(values, current_user)

    out = {i: item for i, item in enumerate(results)}
    return jsonify({"data": out})


async def _scrape_items(request_values: dict[str, str]) -> list[Item]:
    scraper = EmagScraper(
        "https://www.emag.ro/search/",
        request_values["q"],
        int(request_values["search-count"]),
    )
    results = await asyncio.create_task(scraper.get_results())

    ItemDAO.insert_multiple(results, datetime.now())
    return results


def _database_items(request_values: dict[str, str], user: User) -> list[Item]:
    return ItemDAO.get_matching_items(request_values["q"], user)
