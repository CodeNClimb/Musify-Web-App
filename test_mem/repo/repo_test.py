# Author: Mathias Sackey, Sun Lee

import pytest
from datetime import datetime

from main.adapters.abstract_repository import *
from main.models.msac_models import *
from main.models.model import *
from main.models.else_models import *


# test user ________________________________

def test_repo_can_add_user(in_repo):
    user = User('name', 'password1234')
    in_repo.add_user(user)
    assert in_repo.get_user('name') is user

def test_repo_can_get_user(in_repo):
    user1 = in_repo.get_user('user')
    user1 = user1.username + user1.password
    user2 = User('user', 'user')
    user2 = user2.username + user2.password
    assert user1 == user2

def test_repo_does_not_get_non_existent_user(in_repo):
    user = in_repo.get_user('sun lee')
    assert user is None


#test get_by_tracks_by_{} _______________________________________________________

def test_repo_can_get_track(in_repo):
    track1 = Track(1270558,'1792')
    track2 = in_repo.get_track(track1.id)
    assert track1.id == track2.id and track1.name == track2.name

def test_repo_can_get_tracks_by_album(in_repo):
    album = Album(1270, 'Lifestyle')
    track1 = Track(1270558,'1792')
    tracks = in_repo.get_tracks_by_album(album.id)
    assert track1 in tracks

def test_repo_can_get_tracks_by_artist(in_repo):
    artist = Artist(1, 'J-1792')
    track1 = Track(1270558,'1792')
    tracks = in_repo.get_tracks_by_artist(artist.id)
    assert track1 in tracks

def test_repo_can_get_tracks_by_genre(in_repo):
    genre = Genre(692, 'Hip-Hop')
    track1 = Track(1270558,'1792')
    tracks = in_repo.get_tracks_by_genre(genre.id)
    assert track1 in tracks


#test artist _________________________________________________________________

def test_repo_can_get_artist(in_repo):
    artist1 = Artist(3, 'Pure Grease')
    artist2 = in_repo.get_artist(artist1.id)
    assert artist1.id == artist2.id and artist1.name == artist2.name

def test_repo_does_not_get_non_existent_artist(in_repo):
    artist1 = Artist(0, 'cool artist')
    artist2 = in_repo.get_artist(artist1.id)
    assert artist2 is None

def test_repo_can_add_artist(in_repo):
    artist1 = Artist(0, 'New Artist')
    in_repo.add_artist(artist1)
    artist2 = in_repo.get_artist(artist1.id)
    assert artist1.id == artist2.id and artist1.name == artist2.name

#test genre _________________________________________________________________

def test_repo_can_get_genre(in_repo):
    genre1 = Genre(124, 'Blues')
    genre2 = in_repo.get_genre(genre1.id)
    assert genre1.id == genre2.id and genre1.name == genre2.name

def test_repo_does_not_get_non_existent_genre(in_repo):
    genre1 = Genre(0, 'cool new genre')
    genre2 = in_repo.get_genre(genre1.id)
    assert genre2 is None

def test_repo_can_add_genre(in_repo):
    genre1 = Genre(0, 'cool new genre')
    in_repo.add_genre(genre1)
    genre2 = in_repo.get_genre(genre1.id)
    assert genre1.id == genre2.id and genre1.name == genre2.name


#test album _________________________________________________________________

def test_repo_can_get_album(in_repo):
    album1 = Album(1270, 'Lifestyle')
    album2 = in_repo.get_album(album1.id)
    assert album1.id == album2.id and album1.name == album2.name

def test_repo_does_not_get_non_existent_album(in_repo):
    album1 = Album(0, 'Cool New Album')
    album2 = in_repo.get_album(album1.id)
    assert album2 is None

def test_repo_can_add_album(in_repo):
    album1= Album(0, 'Greatest zero album')
    in_repo.add_album(album1)
    album2 = in_repo.get_album(album1.id)
    assert album1.id == album2.id and album1.name == album2.name


#test review _________________________________________________________________

def test_repo_can_add_review(in_repo):
    track = Track(1270558, '1792')
    user = User('mathias', 'password')
    review1 =  Review(datetime.now(), '★★★★★', "Love this track bro", track, user)
    in_repo.get_track(review1.track.id).add_review(review1)
    reviews = in_repo.get_reviews()
    valid = False
    for review in reviews:
        if review == review1:
            valid = True
    assert valid
