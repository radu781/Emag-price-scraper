from aioflask import session
from flask import Blueprint, redirect, make_response
from flask.wrappers import Response
from controllers.user_register import register

from utils.argument_parser import *

user_register_view_blueprint = Blueprint("user_register_view_blueprint", __name__)


@user_register_view_blueprint.route("/register", methods=["POST"])
def user_register() -> Response:
    register()
    return make_response(redirect(session["last_page"]))
