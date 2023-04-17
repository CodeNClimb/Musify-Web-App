# Author: Mathias Sackey, Sun Lee


import pytest

from datetime import datetime
from sqlalchemy.exc import IntegrityError

from main.models.else_models import *
from main.models.model import *
from main.models.msac_models import *

times = datetime.now()


def insert_user(empty_session, values=None):
    new_name = "Andrew"
    new_password = "1234"

    if values is not None:
        new_name = values[0]
        new_password = values[1]

    empty_session.execute('INSERT INTO users (username, password) VALUES (:user_name, :password)',
                          {'user_name': new_name, 'password': new_password})
    row = empty_session.execute('SELECT id from users where username = :user_name',
                                {'user_name': new_name}).fetchone()
    return row[0]

def insert_users(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO users (username, password) VALUES (:user_name, :password)',
                              {'user_name': value[0], 'password': value[1]})
    rows = list(empty_session.execute('SELECT id from users'))
    keys = tuple(row[0] for row in rows)
    return keys

def insert_track(empty_session):
    empty_session.execute(
        'INSERT INTO tracks (id, name, url, img_url, time, artist_id, album_id) VALUES (:id, :name, :url, :img_url, :time, :artist_id, :album_id) ',
        {
            'id': 1234,
            'name': 'new song',
            'url': 'https://www.spotify.com',
            'img_url': 'https://www.spotify.com',
            'time': times.strftime("%H:%M:%S"),
            'artist_id': 1,
            'album_id': 2


        }
    )
    row = empty_session.execute('SELECT id from tracks').fetchone()
    return row[0]

def make_track():
    track = Track(
        id= 1234,
        name= 'new song'
    )
    track.url = 'https://www.spotify.com'
    track.img_url = 'https://www.spotify.com/image'
    return track

def insert_reviewed_track(empty_session):
    track_key = insert_track(empty_session)
    user_key = insert_user(empty_session)

    timestamp_1 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    timestamp_2 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    empty_session.execute(
        'INSERT INTO reviews (user_id, track_id, review, rating, datetime) VALUES '
        '(:user_id, :track_id, "Review 1", "★★☆☆☆", :timestamp_1),'
        '(:user_id, :track_id, "Review 2", "★★★☆☆",:timestamp_2)',
        {'user_id': user_key, 'track_id': track_key, 'timestamp_1': timestamp_1, 'timestamp_2': timestamp_2}
    )

    row = empty_session.execute('SELECT id from tracks').fetchone()
    return row[0]

def make_user():
    user = User("Andrew", "111")
    return user

def test_loading_of_users(empty_session):
    users = list()
    users.append(("Andrew", "1234"))
    users.append(("Cindy", "1111"))
    insert_users(empty_session, users)

    expected = [
        User("Andrew", "1234"),
        User("Cindy", "1111")
    ]
    assert empty_session.query(User).all() == expected

def test_saving_of_users(empty_session):
    user = make_user()
    empty_session.add(user)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT username, password FROM users'))
    assert rows == [("Andrew", "111")]

def test_saving_of_users_with_common_username(empty_session):
    insert_user(empty_session, ("Andrew", "1234"))
    empty_session.commit()

    with pytest.raises(IntegrityError):
        user = User("Andrew", "111")
        empty_session.add(user)
        empty_session.commit()

def test_loading_of_track(empty_session):
    track_key = insert_track(empty_session)
    expected_track = make_track()
    fetched_track = empty_session.query(Track).one()

    assert expected_track == fetched_track
    assert track_key == fetched_track.id

def test_loading_of_reviewed_track(empty_session):
    insert_reviewed_track(empty_session)

    rows = empty_session.query(Track).all()
    track = rows[0]

    for review in track.reviews:
        assert review.track is track

def test_saving_of_reviewed_track(empty_session):
    track = make_track()
    track.time = times.strftime("%H:%M:%S")
    user = make_user()

    review_text = 'Some review text'
    rating = '★★★☆☆'
    review = make_review(review_text, rating, user, track, datetime.now())

    empty_session.add(track)
    empty_session.commit()


    rows = list(empty_session.execute('SELECT id FROM tracks'))
    track_key = rows[0][0]

    rows = list(empty_session.execute('SELECT id FROM users'))
    user_key = rows[0][0]

    rows = list(empty_session.execute('SELECT user_id, track_id, review FROM reviews'))
    assert rows == [(user_key, track_key, review_text)]

def make_review(review_text: str, rating:str, user: User, track: Track, timestamp: datetime):
    review= Review(timestamp, rating, review_text, track, user)
    track.add_review(review)
    user.add_review(review)
    return review

def test_saving_of_review(empty_session):
    track_key = insert_track(empty_session)
    user_key = insert_user(empty_session, ("Andrew", "1234"))

    rows = empty_session.query(Track).all()
    track = rows[0]
    user = empty_session.query(User).filter(User._User__username == "Andrew").one()

    # Create a new Comment that is bidirectionally linked with the User and Article.
    review_text = "Some comment text."
    rating = '★★★☆☆'
    review = make_review(review_text, rating, user, track, datetime.today())

    # Note: if the bidirectional links between the new Comment and the User and
    # Article objects hadn't been established in memory, they would exist following
    # committing the addition of the Comment to the database.
    empty_session.add(review)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT user_id, track_id, review FROM reviews'))

    assert rows == [(user_key, track_key , review_text)]

def test_saving_of_track(empty_session):
    track = make_track()
    track.time = times.strftime("%H:%M:%S")
    empty_session.add(track)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT name, url, img_url, time, artist_id, album_id FROM tracks'))
    assert rows == [(
        'new song',
        'https://www.spotify.com',
        'https://www.spotify.com/image',
        track.time,
        None,
        None
    )]
