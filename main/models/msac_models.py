# main/models/msac_models.py __________________________________________________
# Author: Mathias Sackey, Sun Lee


from main.services import validate_integer, validate_string


# Review ______________________________________________________________________

class Review:
    
    @property
    def datetime(self):
        return self.__datetime

    @property
    def rating(self):
        return self.__rating

    @property
    def review(self):
        return self.__review

    @property
    def track(self):
        return self.__track

    @property
    def user(self):
        return self.__user

    def __init__(self, datetime, rating, review, track, user):
        self.__datetime = datetime
        self.__rating   = rating
        self.__review   = review
        self.__track    = track
        self.__user     = user

    def __eq__(self, __o):
        return isinstance(__o, self.__class__)\
            and __o.datetime == self.datetime\
                and __o.review == self.review
    
    def __repr__(self):
        return f'<Review {self.track.id} {self.user.username}: {self.rating} {self.review}>'


# User ________________________________________________________________________

class User:

    @property
    def username(self):
        return self.__username

    @property
    def password(self):
        return self.__password

    @property
    def reviews(self):
        return self.__reviews
    
    def add_review(self, review):
        self.__reviews.append(review)

    def remove_review(self, review):
        self.__reviews.remove(review)

    def __init__(self, username, password):
        self.__username = validate_string(username)
        self.__password = password
        self.__reviews  = []

    def __eq__(self, __o):
        return isinstance(__o, self.__class__)\
            and __o.username == self.username\
                and __o.password == self.password

    def __repr__(self) :
        return f'<User {self.username}>'