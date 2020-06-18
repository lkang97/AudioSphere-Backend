from flask import Blueprint
from flask_cors import cross_origin
from ..auth import *
from app.models import db, User, Song

bp = Blueprint("comments", __name__, url_prefix='/songs')


@bp.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response
