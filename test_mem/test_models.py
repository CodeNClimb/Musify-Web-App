# test/test_models.py _________________________________________________________
# Author: Sun Lee


import pytest
from datetime import datetime

from main.models.else_models import Tracker, Album, Artist, Genre
from main.models.msac_models import User, Review
from main.models.model import Model, Track


# Test Model __________________________________________________________________
# Inherited by Track, Tracker

class TestModel:

    model1 = Model('1', 'Model')
    model2 = Model(2, ' Model ')
    model3 = Model(3, '')
    model4 = Model(4, 771111001011083252)

    def test_init(self):
        # test id _____________________________________________________________
        assert self.model1.id == 1
        assert self.model2.id == 2

        with pytest.raises(ValueError):
            Model(None, 'Model')
        with pytest.raises(ValueError):
            Model(-1, 'Model')

        # test name _____________________________________________________________
        assert self.model1.name == 'Model'
        assert self.model2.name == 'Model'
        assert self.model3.name == None
        assert self.model4.name == None
    
    def test_eq(self):
        assert self.model1 != 'String'
        assert self.model1 != self.model2

        model1_copy1 = Model(1, 'Model')
        model1_copy2 = Model(1, 'Model Copy')
        assert self.model1 == model1_copy1
        assert self.model1 == model1_copy2

        album   = Album(0, 'Album')
        artist  = Artist(0, 'Artist')
        genre   = Genre(0, 'Genre')
        assert album    != artist
        assert artist   != genre
        assert genre    != album

    def test_lt(self):
        assert self.model1 < self.model2
        assert not(self.model1 > self.model2)

        models = [self.model3, self.model1, self.model2, self.model4]
        assert sorted(models) == [self.model1, self.model2, self.model3, self.model4]

    def test_set(self):
        models = set()
        models.add(self.model1)
        models.add(self.model2)
        models.add(self.model3)
        models.add(self.model4)
        assert sorted(models) == [self.model1, self.model2, self.model3, self.model4]

        models.discard(self.model1)
        assert sorted(models) == [self.model2, self.model3, self.model4]


# Test Track __________________________________________________________________

class TestTrack:

    track = Track(0, 'Track')

    def test_attr(self):
        self.track.url              = ' http://track.co.nz '
        self.track.img_url          = ' http://track.co.nz/image '
        self.track.time             = ' 00:11:22 '
        assert self.track.url       == 'http://track.co.nz'
        assert self.track.img_url   == 'http://track.co.nz/image'
        assert self.track.time      == '00:11:22'

        self.track.url              = ''
        self.track.img_url          = ''
        self.track.time             = ''
        assert self.track.url       == None
        assert self.track.img_url   == None
        assert self.track.time      == None

        self.track.url              = 1
        self.track.img_url          = 1
        self.track.time             = 1
        assert self.track.url       == None
        assert self.track.img_url   == None
        assert self.track.time      == None

        self.track.time         = '-1:-2'
        assert self.track.time  == None

        self.track.time         = '0:a'
        assert self.track.time  == None

        self.track.time         = '0:1:2:3'
        assert self.track.time  == None

    def test_reviews(self):
        review1 = Review(datetime.now(), 'This is a review.', 'xxxoo', Track(1, None), User('user1', 'user1'))
        review2 = Review(datetime.now(), 'This is also a review.', 'xxooo', Track(2, None), User('user2', 'user2'))
        self.track.add_review(review1)
        self.track.add_review(review2)
        assert len(self.track.reviews) == 2
        assert self.track.get_review(review1.user) == review1
        assert self.track.get_review(review2.user) == review2
        assert self.track.get_review(review1.user) != review2

        self.track.remove_review(review1)
        assert self.track.get_review(review1.user) == None


# Test Tracker ________________________________________________________________
# Inherited by Album/Artist/Genre

class TestTracker:

    tracker = Tracker(1, 'Tracker')

    def test_attr(self):
        self.tracker.img_url        = ' http://tracker.co.nz/image '
        assert self.tracker.img_url == 'http://tracker.co.nz/image'

        self.tracker.img_url        = ''
        assert self.tracker.img_url == None

        self.tracker.img_url        = 1
        assert self.tracker.img_url == None

    def test_tracks(self):
        track1 = Track(1, 'Track')
        track2 = Track(2, 'Track')
        self.tracker.add_track(track1)
        self.tracker.add_track(track2)
        assert len(self.tracker.tracks) == 2
        assert self.tracker.get_track(track1.id) == track1
        assert self.tracker.get_track(track2.id) == track2
        assert self.tracker.get_track(track1.id) != track2
