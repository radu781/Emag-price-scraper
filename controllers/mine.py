from . import app
from aioflask import session
from flask import make_response, render_template, request, Blueprint
from utils.item_dao import ItemDAO

mine_blueprint = Blueprint("mine_blueprint", __name__)


@app.route("/mine")
async def mine():
    results = ItemDAO.get_tracked_items_by_user(session.get("user_id", -1))
    template = render_template(
        "mine.html",
        links=results,
        entry_count=len(results),
    )
    response = make_response(template)
    return response
