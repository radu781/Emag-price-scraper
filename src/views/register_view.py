import json
from aioflask import session
from flask import Blueprint, redirect, make_response, render_template
from flask.wrappers import Response

from utils.argument_parser import *
from views.register_inner import register_inner

user_register_view_blueprint = Blueprint("user_register_view_blueprint", __name__)


@user_register_view_blueprint.route("/register", methods=["GET", "POST"])
def user_register() -> Response:
    response = json.loads(register_inner().data)

    if "reason" in response:
        if response["reason"] == "user already exists":
            return make_response(render_template("register.html", reason="That user already exists"))
        if response["reason"] == "passwords are not the same":
            return make_response(render_template("register.html", reason="Passwords are not the same"))

    if not "user_id" in session or session["user_id"] == -1:
        return make_response(render_template("register.html", reason=None))
    return make_response(redirect(session["last_page"]))
