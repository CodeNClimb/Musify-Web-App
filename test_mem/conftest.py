# Author: Mathias Sackey, Sun Lee

import pytest
from main import create_app
from main.adapters.memory_repository import Repository
from main.adapters.services import get_project_root


# Configure data to use test paths  _________________________________ 

TEST_DATA_PATH = get_project_root() / "test_mem" / "data"


# Validators _________________________________________________________________


def validate_integer(id):
    try:
        if int(id) < 0:
            raise ValueError
        return int(id)
    except:
        raise ValueError(f'Invalid ID: {id}')

def validate_string(name):
    try:
        if name.strip() == '':
            raise ValueError
        return name.strip()
    except:
        return None


# _____________________________________________________________________________

import os
import ast
import csv

from main.models.else_models import Album, Artist, Genre
from main.models.msac_models import User, Review
from main.models.model import Track


# Reader + Writer _____________________________________________________________

def read_csv(file):
    with open(file, encoding='utf-8-sig') as f:
        for e in csv.DictReader(f):
            yield e

def write_csv(file, cols, rows):
    with open(file, 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f)
        w.writerow(cols)
        w.writerows(rows)


# Read Tracks _________________________________________________________________

def read_tracks(repo):
    tracks_file = str(os.getcwd()) + '\\test_mem\\data\\tracks.csv'

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
    users_file = str(os.getcwd()) + '\\test_mem\\data\\users.csv'
    for e in read_csv(users_file):
        user = User(e['username'], e['password'])
        repo.add_user(user)


# Read Reviews ________________________________________________________________

def read_reviews(repo):
    reviews_file = str(os.getcwd()) + '\\test_mem\\data\\reviews.csv'

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


# Write Users _________________________________________________________________

def write_users(repo):
    users_file = str(os.getcwd()) + '\\test_mem\\data\\users.csv'
    headers = [
        'username',
        'password'
    ]
    users = [
        [user.username,
        user.password]
        for user in repo.get_users()
    ]
    write_csv(users_file, headers, users)


# Write Reviews _______________________________________________________________

def write_reviews(repo):
    reviews_file = str(os.getcwd()) + '\\test_mem\\data\\reviews.csv'
    headers = [
        'datetime',
        'rating',
        'review',
    ]
    reviews = [
        [review.datetime,
        review.rating,
        review.review,
        review.track.id,
        review.user.username]
        for review in repo.get_reviews()
    ]
    write_csv(reviews_file, headers, reviews)


# test repo setup _________________________________________________

@pytest.fixture
def in_repo():
    repo = Repository()
    read_tracks(repo)
    read_users(repo)
    read_reviews(repo)
    return repo

@pytest.fixture
def client():
    app = create_app({
        'REPOSITORY':   'memory',
        'TESTING':      False
    })
    return app.test_client()

class AuthenticationManager:
    def __init__(self, client):
        self.__client = client

    def sign_in(self, username='mathias', password='123MangoDog'):
        return self.__client.post(
            '/sign-in',
            data={'username': username, 'password': password}
        )

    def sign_out(self):
        return self.__client.get('/sign-out')

@pytest.fixture
def auth(client):
    return AuthenticationManager(client)
