from flask import Blueprint
from flask_cors import cross_origin
from ..auth import *
from app.models import db, User, Song
import requests

bp = Blueprint("favorites", __name__, url_prefix='/songs')


@bp.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


@bp.route('/<int:song_id>/favorites', methods=['PATCH'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def add_favorite(song_id):
    song = Song.query.get(song_id)
    token = request.headers.get('Authorization')
    req = requests.get('https://dev-c-4o8wnx.auth0.com/userinfo',
                       headers={'Authorization': token}).content
    userInfo = json.loads(req)
    user = User.query.filter_by(email=userInfo['email']).first()
    print(user)
    try:
        user.favorites.remove(song)
        db.session.add(user)
        db.session.commit()
        return "Deleted", 204
    except:  # noqa
        user.favorites.append(song)
        db.session.add(user)
        db.session.commit()
        return "Created favorite", 201
