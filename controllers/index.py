from aioflask import session
from flask import make_response, render_template, request, Blueprint
import asyncio
from scraper.emag_scraper import EmagScraper
from scraper.item import Item

from utils.item_dao import ItemDAO
from utils.argument_parser import ArgType, Argument, ArgumentParser, Method
from controllers.base import app

index_blueprint = Blueprint("index_blueprint", __name__)


@index_blueprint.route("/", methods=["GET", "POST"])
async def index():
    session["user_id"] = 1
    if request.method == "GET":
        parser = ArgumentParser(
            request,
            {
                Argument("q", ArgType.Mandatory, None),
                Argument("search-count", ArgType.Optional, -1),
                Argument("price-min", ArgType.Optional, 0),
                Argument("price-max", ArgType.Optional, 10_000),
            },
        )
        values = parser.get_values()

        scraper = EmagScraper(
            "https://www.emag.ro/search/", values["q"], int(values["search-count"])
        )
        results = await asyncio.create_task(scraper.get_results())
        ItemDAO.insert_multiple(results)
        completed: list[Item] = []
        for result in results:
            for item in ItemDAO.add_id(result):
                completed.append(item)
        results = completed
        template = render_template(
            "index.html",
            links=results,
            entry_count=len(results),
        )
        response = make_response(template)
        return response
    else:
        parser = ArgumentParser(
            request, {Argument("track", ArgType.Similar, None)}, Method.Post
        )
        values = parser.get_values()
        ItemDAO.add_tracked_item_to_user(
            int(values["track"]), int(session.get("user_id", -1))
        )
        return values
