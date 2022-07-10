from aioflask import session
from flask import make_response, render_template, request, Blueprint, redirect
import asyncio

from scraper.emag_scraper import EmagScraper
from scraper.item import Item
from utils.item_dao import ItemDAO
from utils.argument_parser import *
from utils.user import User
from utils.user_dao import UserDAO

index_blueprint = Blueprint("index_blueprint", __name__)


@index_blueprint.route("/", methods=["GET", "POST"])
async def index():
    if request.method == "GET":
        parser = ArgumentParser(
            request,
            {
                Argument("q", ArgType.Optional, None),
                Argument("search-count", ArgType.Optional, "-1"),
                Argument("price-min", ArgType.Optional, 0),
                Argument("price-max", ArgType.Optional, 10_000),
            },
        )
        values = parser.get_values()
        if values["q"] is None:
            return render_template("index.html")

        results = await __search_items(values)

        current_user = None
        user_id = session.get("user_id", None)
        if user_id is not None:
            current_user = UserDAO.get_user(user_id)

        template = render_template(
            "index.html",
            links=results,
            entry_count=len(results),
            user=current_user,
        )
        response = make_response(template)
        return response
    elif request.method == "POST":
        parser = ArgumentParser(
            request,
            {
                # Argument("track", ArgType.Similar, None),
                Argument("user-name", ArgType.Optional, None),
                Argument("user-password", ArgType.Optional, None),
                Argument("logout", ArgType.Optional, None),
            },
            Method.Post,
        )
        values = parser.get_values()
        # ItemDAO.add_tracked_item_to_user(
        #     int(values["track"]), int(session.get("user_id", -1))
        # )
        if values["logout"] is not None:
            session.pop("user_id", None)
            return render_template("index.html", user=None)
        else:
            current_user = User(values["user-name"], values["user-password"])
            current_user = __get_user_status(current_user)
            user_id = UserDAO.get_user_id(current_user)
            if user_id != -1:
                session["user_id"] = user_id
                return render_template("index.html", user=current_user)
            return redirect(request.url)
            template = render_template("index.html", user=None)
            return make_response(template)


async def __search_items(values):
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
    user.status = User.Status.LoggedOut

    if not UserDAO.exists(user):
        user.status = User.Status.NameMismatch
    if not UserDAO.correct_credentials(user):
        user.status = User.Status.PasswordMismatch

    return user
