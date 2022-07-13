from aioflask import session
from flask import request, Blueprint, redirect
from utils.item_dao import ItemDAO

from utils.argument_parser import *
from . import _get_current_user

track_item_blueprint = Blueprint("track_item_blueprint", __name__)


@track_item_blueprint.route("/track", methods=["POST"])
def track_item():
    if request.method == "POST":
        parser = ArgumentParser(
            request,
            {
                Argument("unset", ArgType.Prefix, None),
                Argument("set", ArgType.Prefix, None),
            },
            Method.Post,
        )
        values = parser.get_values()
        current_user = _get_current_user(session)
        if current_user.ok:
            if "unset" in values:
                values["unset"] = values["unset"].replace(".x", "").replace(".y", "")
                ItemDAO.remove_tracked_item_from_user(
                    values["unset"], session["user_id"]
                )
                return redirect(session["last_page"])
            elif "set" in values:
                values["set"] = values["set"].replace(".x", "").replace(".y", "")
                ItemDAO.add_tracked_item_to_user(values["set"], session["user_id"])
                return redirect(session["last_page"])
            else:
                return "fail"
        else:
            return "fail"
