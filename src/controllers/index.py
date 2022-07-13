import json
from aioflask import session
from flask import Blueprint, make_response, render_template, request
from flask.wrappers import Response

from scraper.item import Item
from utils.argument_parser import *
from utils.user import User
from utils.user_dao import UserDAO

from controllers.api.search_items import search

index_blueprint = Blueprint("index_blueprint", __name__)


@index_blueprint.route("/", methods=["GET", "POST"])
async def index() -> Response:
    session["last_page"] = request.url
    response = await search()

    json_response = json.loads(response.data)
    data = json_response["data"]
    user = User.from_dict(json_response["user"])
    items = {Item.from_dict(data[item]) for item in data}

    return make_response(
        render_template(
            "index.html",
            links=items,
            entry_count=len(items),
            user=user,
        )
    )


def __get_user_status(user: User) -> User:
    user.status = User.Status.LoggedIn

    if not UserDAO.exists(user):
        user.status = User.Status.NameMismatch
    if not UserDAO.correct_credentials(user):
        user.status = User.Status.PasswordMismatch

    return user
