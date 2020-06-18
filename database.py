from dotenv import load_dotenv
load_dotenv()

from server import app  # noqa
from app.models import db, User, Song, Comment  # noqa

with app.app_context():
    db.drop_all()
    db.create_all()

    user1 = User(nickname="demo", email="demo@demo.com")
    song1 = Song(title="Song 1",
                 genre="Rap",
                 description="description 1",
                 image_url="image placeholder",
                 song_url="song placeholder",
                 user_id=1,
                 created_at="2020-06-06 16:56:54.271262")
    song2 = Song(title="Category 2",
                 genre="Pop",
                 description="description 2",
                 image_url="image placeholder 2",
                 song_url="song placeholder 2",
                 user_id=1,
                 created_at="2020-06-06 16:56:54.271262")
    comment1 = Comment(comment="comment 1",
                       user_id=1,
                       song_id=1)
    comment2 = Comment(comment="comment 2",
                       user_id=1,
                       song_id=2)

    db.session.add(user1)
    db.session.add(song1)
    db.session.add(song2)
    db.session.add(comment1)
    db.session.add(comment2)
    # db.session.add(user1)
    # db.session.add(cat1)
    # db.session.add(cat2)
    # db.session.add(set1)
    # db.session.add(set2)
    # db.session.add(card1)
    # db.session.add(card2)
    # db.session.add(card3)
    # db.session.add(card4)
    # db.session.add(card5)
    # db.session.add(card6)
    # db.session.add(card7)
    db.session.commit()
