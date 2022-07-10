from . import _get_current_user
from aioflask import session
from flask import make_response, render_template, Blueprint
from utils.item_dao import ItemDAO

mine_blueprint = Blueprint("mine_blueprint", __name__)


@mine_blueprint.route("/mine")
async def mine():
    current_user = _get_current_user(session)
    if current_user is None:
        return "broken"
    results = ItemDAO.get_tracked_items_by_user(current_user.id_)
    template = render_template(
        "mine.html",
        links=results,
        entry_count=len(results),
        user=current_user
    )
    response = make_response(template)
    return response
