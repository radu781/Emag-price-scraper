from aioflask import session
from flask import Blueprint, redirect, make_response
from controllers.user_login import login
from flask.wrappers import Response

from utils.argument_parser import *

user_login_view_blueprint = Blueprint("user_login_view_blueprint", __name__)


@user_login_view_blueprint.route("/login", methods=["POST"])
def user_login() -> Response:
    login()
    return make_response(redirect(session["last_page"]))
