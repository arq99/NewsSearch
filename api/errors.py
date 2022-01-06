import werkzeug.exceptions
from flask import Blueprint, Response

errors = Blueprint("errors", __name__)


@errors.app_errorhandler(Exception)
def server_error(error):
    print(error)
    return Response(f"Oops, got an error! {error}", status=500)


@errors.app_errorhandler(werkzeug.exceptions.MethodNotAllowed)
def handle_method_not_allowed(error):
    return Response(f"Oops, got an error! {error}", status=405)


@errors.app_errorhandler(werkzeug.exceptions.BadRequest)
def handle_bad_request(error):
    return Response(f"Oops, got an error! {error}", status=400)
