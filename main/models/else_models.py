# main/models/else_models.py __________________________________________________
# Author: Sun Lee


from main.models.model import Model
from main.services import validate_string


# Template Album/Artist/Genre  ________________________________________________

class Tracker(Model):

    # members #

    # tracks
    @property
    def tracks(self):
        return self.__tracks


    # methods #

    def add_track(self, track):
        self.tracks[track.id] = track

    def get_track(self, i):
        return self.tracks.get(i)
    
    def __init__(self, id, name):
        super().__init__(id, name)
        self.__tracks   = {}
        self.img_url    = None


# Album _______________________________________________________________________

class Album(Tracker):

    def __init__(self, id, name):
        super().__init__(id, name)


# Artist ______________________________________________________________________

class Artist(Tracker):

    def __init__(self, id, name):
        super().__init__(id, name)


# Genre _______________________________________________________________________

class Genre(Tracker):

    def __init__(self, id, name):
        super().__init__(id, name)
