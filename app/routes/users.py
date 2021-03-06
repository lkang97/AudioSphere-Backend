from flask import Blueprint
from flask_cors import cross_origin
from ..auth import *
from app.models import db, User, Song
import requests

bp = Blueprint("users", __name__, url_prefix='/users')


@bp.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


@bp.route('')
def user():
    return "Get user"


@bp.route('/private')
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def privateUser():
    return "Private user endpoint"


# This route will create a new user within the audiosphere database
@bp.route('', methods=['POST'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def updateUser():
    body = request.json
    # Checks if there there is already a user in db
    db_user = User.query.filter_by(email=body['email']).first()
    if db_user:  # If user exists updates the user's nickname
        db_user.nickname = body['nickname']
        return jsonify({'userId': db_user.id}), 201
    else:  # If not, create a new user
        new_user = User(email=body['email'],
                        nickname=body['nickname']
                        )
        db.session.add(new_user)
        db.session.commit()

        return 'User created', 201


# This route will get all the songs for a specific user
@bp.route('/songs')
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def userSongs():
    token = request.headers.get('Authorization')
    req = requests.get('https://dev-c-4o8wnx.auth0.com/userinfo',
                       headers={'Authorization': token}).content
    userInfo = json.loads(req)
    userId = User.query.filter_by(email=userInfo['email']).first().id
    userInfo = User.query.options(db.joinedload(
        'songs'), db.joinedload('favorites')).get(userId)
    return userInfo.to_dict(), 200
