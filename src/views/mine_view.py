import json
from aioflask import session
from flask import make_response, render_template, Blueprint
from controllers.mine import mine
from flask.wrappers import Response

from models.item import Item
from models.user import User

mine_view_blueprint = Blueprint("mine_view_blueprint", __name__)


@mine_view_blueprint.route("/mine")
def mine_page() -> Response:
    response = mine()
    json_response = json.loads(response.data)
    try:
        data = json_response["data"]
        items = {Item.from_dict(item) for item in data}
        current_user = User.from_dict(json_response["user"])
        return make_response(
            render_template(
                "mine.html", links=items, entry_count=len(items), user=current_user
            )
        )
    except KeyError:
        return make_response("broken")
