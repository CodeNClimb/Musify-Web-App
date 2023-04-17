# main/adapters/repository.py ________________________________________________
# Author: Sun Lee


from operator import and_
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.exc import NoResultFound

from main.adapters.abstract_repository import AbstractRepository
from main.models.else_models import Album, Artist, Genre
from main.models.msac_models import User, Review
from main.models.model import Track


class Database:

    # members _________________________________________________________________

    @property
    def session(self):
        return self.__session


    # methods _________________________________________________________________

    def __init__(self, session):
        self.__session = scoped_session(session)
        self.__session_factory = session

#    def __enter__(self):
#        return self
    
#    def __exit__(self, *args):
#        self.rollback()


#    def rollback(self):
#        self.session.rollback()

    def close_session(self):
        if self.session:
            self.session.close()

    def reset_session(self):
        self.close_session()
        self.__session = scoped_session(self.__session_factory)


class Repository(AbstractRepository):

    def __init__(self, session):
        self._db = Database(session)
    
    def close_session(self):
        self._db.close_session()

    def reset_session(self):
        self._db.reset_session()

    # Tracks __________________________________________________________________

    def get_track(self, id):
        return self._db.session.query(Track).get(id)

    def get_tracks(self):
        return self._db.session.query(Track).all()

    def get_tracks_by_album(self, id):
        return self.get_album(id).tracks
    
    def get_tracks_by_artist(self, id):
        return self.get_artist(id).tracks
    
    def get_tracks_by_genre(self, id):
        return self.get_genre(id).tracks

    def add_track(self, track):
        self._db.session.add(track)
        self._db.session.commit()


    # Albums __________________________________________________________________
    
    def get_album(self, id):
        return self._db.session.query(Album).get(id)

    def get_albums(self):
        return self._db.session.query(Album).all()

    def add_album(self, album):
        self._db.session.add(album)
        self._db.session.commit()


    # Artists _________________________________________________________________

    def get_artist(self, id):
        return self._db.session.query(Artist).get(id)

    def get_artists(self):
        return self._db.session.query(Artist).all()

    def add_artist(self, artist):
        self._db.session.add(artist)
        self._db.session.commit()


    # Genres __________________________________________________________________

    def get_genre(self, id):
        return self._db.session.query(Genre).get(id)

    def get_genres(self):
        return self._db.session.query(Genre).all()

    def add_genre(self, genre):
        self._db.session.add(genre)
        self._db.session.commit()


    # Users ___________________________________________________________________

    def get_user(self, username):
        try:
            return self._db.session.query(User)\
                .filter(User._User__username == username)\
                    .one()
        except NoResultFound:
            return None

    def get_users(self):
        return self._db.session.query(User).all()

    def add_user(self, user):
        self._db.session.add(user)
        self._db.session.commit()


    # Reviews _________________________________________________________________

    def get_review(self, track, user):
        try:
            return self._db.session.query(Review)\
                .filter(and_(
                    Review._Review__track == track,
                    Review._Review__user == user
                )).one()
        except NoResultFound:
            return None

    def get_reviews(self):
        return self._db.session.query(Review).all()

    def get_reviews_by_track(self, id):
        return self.get_track(id).reviews

    def add_review(self, review):
        self._db.session.add(review)
        self._db.session.commit()