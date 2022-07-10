from aioflask import session
from flask import request, Blueprint, redirect

from utils.argument_parser import *

user_logout_blueprint = Blueprint("user_logout_blueprint", __name__)


@user_logout_blueprint.route("/logout", methods=["POST"])
def user_logout():
    if request.method == "POST":
        parser = ArgumentParser(
            request,
            {
                Argument("logout", ArgType.Mandatory, None),
            },
            Method.Post,
        )
        values = parser.get_values()
        if values["logout"] == "logout":
            session.pop("user_id", None)
            session.pop("user_status", None)
            return redirect("/")
