# Author: Mathias Sackey, Sun Lee


import pytest
import os
import ast
import time
from datetime import datetime

from main.adapters.database_repository import *
from main.models.msac_models import *
from main.models.model import *
from main.models.else_models import *
from main.adapters.services import read_csv
from test_db.unit.test_orm import make_review


# Read Tracks _________________________________________________________________

def read_tracks(repo):
    tracks_file = str(os.getcwd()) + '\\test_db\\data\\tracks.csv'

    for e in read_csv(tracks_file):

        # artists
        artist = repo.get_artist(validate_integer(e['artist_id']))
        if not artist:
            artist =            Artist(e['artist_id'], e['artist_name'])
            artist.img_url =    e['artist_img_url']
            repo.add_artist(artist)

        # albums
        album = repo.get_album(validate_integer(e['album_id']))
        if not album:
            album =             Album(e['album_id'], e['album_name'])
            album.img_url =     e['album_img_url']
            repo.add_album(album)

        # genres
        genres = []
        for g in ast.literal_eval(e['track_genres']):
            genre = repo.get_genre(validate_integer(g['genre_id']))
            if not genre:
                genre =         Genre(g['genre_id'], g['genre_name'])
                genre.img_url = '/static/album.jpg'
                repo.add_genre(genre)
            genres.append(genre)

        # tracks
        track = repo.get_track(validate_integer(e['track_id']))
        if not track:
            track =             Track(e['track_id'], e['track_name'])
            track.url =         e['track_url']
            track.img_url =     e['track_img_url']
            track.time =        e['track_time']
        track.album =           album
        track.artist =          artist
        track.genres =          genres
        repo.add_track(track)

    print('Tracks:  ', len(repo.get_tracks()))
    print('Albums:  ', len(repo.get_albums()))
    print('Aritsts: ', len(repo.get_artists()))
    print('Genres:  ', len(repo.get_genres()))
    print()


# Read Users __________________________________________________________________

def read_users(repo):
    users_file = str(os.getcwd()) + '\\test_db\\data\\users.csv'
    for e in read_csv(users_file):
        user = User(e['username'], e['password'])
        repo.add_user(user)


# Read Reviews ________________________________________________________________

def read_reviews(repo):
    reviews_file = str(os.getcwd()) + '\\test_db\\data\\reviews.csv'

    for e in read_csv(reviews_file):
        track = repo.get_track(validate_integer(e['track_id']))
        user =  repo.get_user(validate_string(e['user_name']))
        if not repo.get_review(track, user):
            review = Review(
                e['datetime'],
                e['rating'],
                e['review'],
                track, user
            )
            repo.add_review(review)

    print('Reviews: ', len(repo.get_reviews()))



# Test Repository _____________________________________________________________

def test_repository_can_add_a_user(session_factory):
    repo = Repository(session_factory)

    read_users(repo)
    read_tracks(repo)
    read_reviews(repo)

    user = User('Dave', '123456789')
    repo.add_user(user)

    repo.add_user(User('Martin', '123456789'))

    user2 = repo.get_user('Dave')

    assert user2 == user and user2 is user

def test_repository_can_retrieve_a_user(session_factory):
    repo = Repository(session_factory)
    
    read_users(repo)
    read_tracks(repo)
    read_reviews(repo)
    
    user = repo.get_user('admin')
    assert user == User('admin', 'admin')

def test_repository_does_not_retrieve_a_non_existent_user(session_factory):
    repo = Repository(session_factory)
    
    read_users(repo)
    read_tracks(repo)
    read_reviews(repo)

    user = repo.get_user('prince')
    assert user is None

def test_repository_can_retrieve_track_count(session_factory):
    repo = Repository(session_factory)
    read_users(repo)
    read_tracks(repo)
    read_reviews(repo)

    number_of_tracks = len(repo.get_tracks())

    assert number_of_tracks == 12

def test_repo_can_add_track(session_factory):
    repo = Repository(session_factory)
    read_users(repo)
    read_tracks(repo)
    read_reviews(repo)

    number_of_tracks = len(repo.get_tracks())
    new_track_id = number_of_tracks + 1
    
    track = Track(
        new_track_id, "Cool song"
    )
    track.url = 'https://www.spotify.com'
    track.img_url = 'https://www.spotify.com/image'
    track.time = time.time()
    repo.add_track(track)

    assert repo.get_track(new_track_id) == track

def test_repo_can_retrieve_track(session_factory):
    repo = Repository(session_factory)
    read_users(repo)
    read_tracks(repo)
    read_reviews(repo)

    track = repo.get_track(46311)
    assert track.name == 'My 600'

    review1 = [review for review in track.reviews if review.review == 'Bad.'][0]
    assert review1.user.username == 'user1'

def test_repository_does_not_retrieve_a_non_existent_article(session_factory):
    repo = Repository(session_factory)
    read_users(repo)
    read_tracks(repo)
    read_reviews(repo)

    track = repo.get_track(123)
    assert track is None

def test_repository_can_add_a_review(session_factory):
    repo = Repository(session_factory)

    read_users(repo)
    read_tracks(repo)
    read_reviews(repo)

    user = repo.get_user('user')
    track = repo.get_track(1270558)

    review = make_review("Cool track who this!",'★★★☆☆', user, track, datetime.now())

    repo.add_review(review)

    assert review in repo.get_reviews()

def test_repository_does_not_add_a_review_without_a_user(session_factory):
    repo = Repository(session_factory)
    read_users(repo)
    read_tracks(repo)
    read_reviews(repo)

    track = repo.get_track(182066)

    with pytest.raises(Exception):
        review = make_review("Cool track who this!",'★★★☆☆', None, track, datetime.now())
        repo.add_review(review)

def test_repository_does_not_add_a_review_without_a_track(session_factory):
    repo = Repository(session_factory)
    read_users(repo)
    read_tracks(repo)
    read_reviews(repo)

    user = repo.get_user('mathias')

    with pytest.raises(Exception):
        review = make_review("Cool track who this!",'★★★☆☆', user, None, datetime.now())
        repo.add_review(review)

def test_repository_can_retrieve_reviews(session_factory):
    repo = Repository(session_factory)
    read_tracks(repo)
    read_users(repo)
    read_reviews(repo)
    print(repo.get_reviews())
    assert len(repo.get_reviews()) == 3

""""""