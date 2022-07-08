from aioflask import session
from flask import make_response, render_template, request, Blueprint
import asyncio
from scraper.emag_scraper import EmagScraper
from scraper.item import Item

from utils.item_dao import ItemDAO
from utils.argument_parser import ArgType, Argument, ArgumentParser, Method
from utils.user import User
from utils.user_dao import UserDAO

index_blueprint = Blueprint("index_blueprint", __name__)


@index_blueprint.route("/", methods=["GET", "POST"])
async def index():
    if request.method == "GET":
        parser = ArgumentParser(
            request,
            {
                Argument("q", ArgType.Mandatory, None),
                Argument("search-count", ArgType.Optional, "-1"),
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
        current_user = None
        if user := session.get("user_id", None) is not None:
            current_user = UserDAO.get_user(user)
        template = render_template(
            "index.html",
            links=results,
            entry_count=len(results),
            user_email=current_user.name if current_user is not None else None,
            user_status="OK",
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
            },
            Method.Post,
        )
        values = parser.get_values()
        # ItemDAO.add_tracked_item_to_user(
        # int(values["track"]), int(session.get("user_id", -1))
        # )
        current_user = User(values["user-name"], values["user-password"])
        user_status = "OK"
        if not UserDAO.exists(current_user):
            user_status = "User does not exist"
        if not UserDAO.correct_credentials(current_user):
            user_status = "Password incorrect"
        session.permanent = False
        session["user_id"] = UserDAO.get_user_id(current_user)
        template = render_template(
            "index.html", user_status=user_status, user_email=current_user.name
        )
        return make_response(template)
