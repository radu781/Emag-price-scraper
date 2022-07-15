import json

from controllers.item_page import item
from flask import Blueprint, make_response, render_template
from flask.wrappers import Response
from models.user import User

item_page_view_blueprint = Blueprint("item_page_view_blueprint", __name__)


@item_page_view_blueprint.route("/item/<item_id>")
def item_page(item_id: str) -> Response:
    response = item(item_id)

    json_response = json.loads(response.data)
    try:
        data = json_response["data"]
        user = User.from_dict(json_response["user"])
        image = json_response["image"]

        return make_response(
            render_template("item.html", user=user, links=data, image=image)
        )
    except KeyError:
        return make_response(
            render_template("item.html", user=User.from_dict(json_response))
        )
