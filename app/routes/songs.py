from flask import Blueprint
from flask_cors import cross_origin
from ..auth import *
from app.models import db, Song
import json

bp = Blueprint("songs", __name__, url_prefix='/songs')


@bp.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


# Returns all the songs in the database
@bp.route('')
def get_songs():
    songs = Song.query.all()
    return jsonify([song.to_dict() for song in songs])


# Returns the information for a single song
@bp.route('/<int:song_id>')
@cross_origin(headers=["Content-Type", "Authorization"])
def single_song(song_id):
    song = Song.query.get(song_id)
    return song.to_dict(), 200


# Creates a new song
@bp.route('', methods=['POST'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def add_song():
    data = request.json
    song = Song(title=data['title'],
                genre=data['genre'],
                description=data['description'],
                image_url=data['image_url'],
                song_url=data['song_url'],
                user_id=data['user_id'],
                created_at=data['created_at'])

    db.session.add(song)
    db.session.commit()
    return song.to_dict(), 201


# Updates a song based on its id
# @bp.route('/<int:song_id>', methods=['PATCH'])
# @cross_origin(headers=["Content-Type", "Authorization"])
# @requires_auth
# def update_song(song_id):
