from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

favorites_table = db.Table('favorites', db.Model.metadata,
        db.Column('user_id', db.Integer, db.ForeignKey('users.id'), nullable=False),  # noqa
        db.Column('song_id', db.Integer, db.ForeignKey('songs.id'), nullable=False))  # noqa


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    nickname = db.Column(db.String(50), nullable=False)

    songs = db.relationship('Song', back_populates='user')
    favorites = db.relationship('Song', secondary=favorites_table)
    comments = db.relationship('Comment', back_populates='user')

    def to_dict(self):
        return {
            "id": self.id,
            'email': self.email,
            'nickname': self.nickname,
            'userSongs': [song.to_dict() for song in self.songs],
            'faveSongs': [favorite.to_dict() for favorite in self.favorites]
        }

    def to_dict_name(self):
        return {
            'nickname': self.nickname
        }

    def to_dict_favorites(self):
        return {
            'id': self.id
        }


class Song(db.Model):
    __tablename__ = 'songs'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    genre = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String)
    song_url = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime)

    user = db.relationship('User', back_populates='songs')
    favorites = db.relationship('User', secondary=favorites_table)
    comments = db.relationship('Comment', back_populates='song')

    def to_dict(self):
        return {
            "id": self.id,
            'title': self.title,
            'genre': self.genre,
            'description': self.description,
            'image_url': self.image_url,
            'song_url': self.song_url,
            'user_id': self.user_id,
            'created_at': self.created_at,
            'favorites': [favorite.to_dict_favorites() for favorite in self.favorites],
            'user': self.user.to_dict_name()
        }


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    song_id = db.Column(db.Integer, db.ForeignKey('songs.id'), nullable=False)

    user = db.relationship('User', back_populates='comments')
    song = db.relationship('Song', back_populates='comments')

    def to_dict(self):
        return {
            'id': self.id,
            'comment': self.comment,
            'user': self.user.to_dict_name(),
        }
