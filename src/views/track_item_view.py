from aioflask import session
from flask import Blueprint, make_response, redirect
from flask.wrappers import Response
from controllers.track_items import track_item

from utils.argument_parser import *


track_item_view_blueprint = Blueprint("track_item_view_blueprint", __name__)


@track_item_view_blueprint.route("/track", methods=["GET", "POST"])
async def track() -> Response:
    track_item()
    return make_response(redirect(session["last_page"]))
