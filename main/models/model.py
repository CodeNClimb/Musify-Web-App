# main/model/model.py _________________________________________________________
# Author: Sun Lee


import re

from main.services import validate_integer, validate_string


# Template Model ______________________________________________________________

class Model:

    # members #

    # id
    @property
    def id(self):
        return self.__id
    @id.setter
    def id(self, id):
        self.__id = validate_integer(id)

    # name
    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self, name):
        self.__name = validate_string(name)

    # url
    @property
    def url(self):
        return self.__url
    @url.setter
    def url(self, url):
        self.__url = validate_string(url)

    # img url
    @property
    def img_url(self):
        return self.__img_url
    @img_url.setter
    def img_url(self, img_url):
        self.__img_url = validate_string(img_url)


    # methods #

    def __init__(self, id, name):
        self.id = id
        self.name = name
    
    def __eq__(self, __o):
        return isinstance(__o, self.__class__) and __o.id == self.id
    
    def __lt__(self, __o):
        return not isinstance(__o, self.__class__) or __o.id > self.id

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.id}: {self.name}>'


# Track _______________________________________________________________________

class Track(Model):

    # members #

    # time
    @property
    def time(self):
        return self.__time
    @time.setter
    def time(self, time):
        # xx:xx:xx
        self.__time = None
        time        = validate_string(time)

        if time:
            h = m = s = '0'
            try:
                m,s = time.split(':')
            except:
                try:
                    h,m,s = time.split(':')
                except:
                    return
            if h.isdigit() and m.isdigit() and s.isdigit():
                self.__time = time
    
    # album
    @property
    def album(self):
        return self.__album
    @album.setter
    def album(self, album):
        self.__album = album

    # artist
    @property
    def artist(self):
        return self.__artist
    @artist.setter
    def artist(self, artist):
        self.__artist = artist

    # genres
    @property
    def genres(self):
        return self.__genres
    @genres.setter
    def genres(self, genres):
        self.__genres = genres

    # reviews
    @property
    def reviews(self):
        return self.__reviews


    # methods #

    def add_review(self, review):
        self.__reviews.append(review)
    
    def remove_review(self, review):
        self.__reviews.remove(review)
    
    def get_review(self, user):
        return next((review for review in self.__reviews if review.user.username == user.username), None)

    def __init__(self, id, name):
        super().__init__(id, name)
        self.__reviews  = []
        self.url        = None
        self.img_url    = None
        self.time       = None
        self.album      = None
        self.artist     = None
        self.genres     = []
