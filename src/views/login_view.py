import json
from aioflask import session
from flask import Blueprint, render_template, make_response, redirect
from flask.wrappers import Response
from models.user import User

from utils.argument_parser import *
from views.login_inner import login_inner

user_login_view_blueprint = Blueprint("user_login_view_blueprint", __name__)


@user_login_view_blueprint.route("/login", methods=["GET", "POST"])
def user_login() -> Response:
    response = json.loads(login_inner().data)

    if "reason" in response:
        actual_reason = User.Status.from_string(response["reason"])
        return make_response(render_template("login.html", reason=actual_reason))

    if not "user_id" in session or session["user_id"] == -1:
        return make_response(render_template("login.html", reason=None))
    return make_response(redirect(session["last_page"]))
