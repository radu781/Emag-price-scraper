import asyncio
from aioflask import session
from flask import Blueprint, make_response, render_template, request
from flask.wrappers import Response

from . import _get_current_user
from scraper.emag_scraper import EmagScraper
from scraper.item import Item
from utils.argument_parser import *
from utils.item_dao import ItemDAO
from utils.user import User
from utils.user_dao import UserDAO

index_blueprint = Blueprint("index_blueprint", __name__)


@index_blueprint.route("/", methods=["GET", "POST"])
async def index() -> Response:
    if request.method == "GET":
        parser = ArgumentParser(
            request,
            {
                Argument("q", ArgType.Optional, None),
                Argument("search-count", ArgType.Optional, 50),
                Argument("price-min", ArgType.Optional, 0),
                Argument("price-max", ArgType.Optional, 10_000),
            },
        )

        current_user = _get_current_user(session)
        current_user.status = User.Status.from_value(session.get("user_status", 3))

        values = parser.get_values()
        if values["q"] is None:
            return make_response(render_template("index.html", user=current_user))

        results = await __search_items(values)
        results = ItemDAO.add_tracking(results, current_user)

        return make_response(
            render_template(
                "index.html",
                links=results,
                entry_count=len(results),
                user=current_user,
            )
        )
    elif request.method == "POST":
        parser = ArgumentParser(
            request,
            {
                Argument("track", ArgType.Prefix, None),
            },
            Method.Post,
        )
        values = parser.get_values()
        current_user = _get_current_user(session)
        ItemDAO.add_tracked_item_to_user(int(values["track"]), current_user.id_)
        template = render_template("mine.html", user=current_user)
        return make_response(template)

    return make_response(render_template("index.html"))


async def __search_items(values: dict[str, str]) -> list[Item]:
    scraper = EmagScraper(
        "https://www.emag.ro/search/", values["q"], int(values["search-count"])
    )
    results = await asyncio.create_task(scraper.get_results())

    ItemDAO.insert_multiple(results)
    completed: list[Item] = []
    for result in results:
        for item in ItemDAO.add_id(result):
            completed.append(item)

    return completed


def __get_user_status(user: User) -> User:
    user.status = User.Status.LoggedIn

    if not UserDAO.exists(user):
        user.status = User.Status.NameMismatch
    if not UserDAO.correct_credentials(user):
        user.status = User.Status.PasswordMismatch

    return user
