from utils.etc import sieve_prices
from . import _get_current_user
from aioflask import session
from flask import make_response, render_template, Blueprint
from utils.item_dao import ItemDAO

item_page_blueprint = Blueprint("item_page_blueprint", __name__)


@item_page_blueprint.route("/item/<item_id>")
def item_page(item_id: str):
    session["last_page"] = "/item"
    current_user = _get_current_user(session)
    if current_user is None:
        return "broken"
    results = ItemDAO.get_all_prices(item_id)
    results = sieve_prices(results)
    image = ItemDAO.get_image(item_id)
    return make_response(
        render_template(
            "item.html", links=results, entry_count=len(results), user=current_user, image=image
        )
    )
