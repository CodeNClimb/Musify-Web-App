# main/adapters/services.py  _________________________________________________
# Author: Sun Lee, Mathias Sackey


import os
import ast
import csv
import time
from pathlib import Path
from wsgiref import validate

from main.models.else_models import Album, Artist, Genre
from main.models.msac_models import User, Review
from main.models.model import Track
from main.services import validate_integer, validate_string


def get_project_root():
    return Path(__file__).parent


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
    tracks_file = str(os.getcwd()) + '\\main\\data\\tracks.csv'

    prev_artist =   None
    before =        time.time()

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

        if prev_artist != artist and artist.id % 10 == 0:
            prev_artist = artist
            print(f'REPOSITORY...{artist.id}%')

    after = time.time() - before
    print(f'\n=== COMPLETED REPOSITORY in {after:.3f}s ===\n')

    print('Tracks:  ', len(repo.get_tracks()))
    print('Albums:  ', len(repo.get_albums()))
    print('Aritsts: ', len(repo.get_artists()))
    print('Genres:  ', len(repo.get_genres()))
    print()


# Read Users __________________________________________________________________

def read_users(repo):
    users_file = str(os.getcwd()) + '\\main\\data\\users.csv'

    for e in read_csv(users_file):
        if not repo.get_user(e['username']):
            user = User(e['username'], e['password'])
            repo.add_user(user)

    print('Users:   ', len(repo.get_users()))


# Read Reviews ________________________________________________________________

def read_reviews(repo):
    reviews_file = str(os.getcwd()) + '\\main\\data\\reviews.csv'

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
    users_file = str(os.getcwd()) + '\\main\\data\\users.csv'

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
    reviews_file = str(os.getcwd()) + '\\main\\data\\reviews.csv'

    headers = [
        'datetime',
        'rating',
        'review',
        'track_id',
        'user_name'
    ]
    reviews = []
    for review in repo.get_reviews():
        try:
            reviews.append([
                review.datetime,
                review.rating,
                review.review,
                review.track.id,
                review.user.username
            ])
        except:
            pass

    write_csv(reviews_file, headers, reviews)