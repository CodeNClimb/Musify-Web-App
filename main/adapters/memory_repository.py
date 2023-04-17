# main/adapters/repository.py ________________________________________________
# Author: Sun Lee, Mathias Sackey


from main.adapters.abstract_repository import AbstractRepository


class Repository(AbstractRepository):

    def __init__(self):
        self.__albums   = {}
        self.__artists  = {}
        self.__genres   = {}
        self.__users    = []

    # Tracks __________________________________________________________________

    def get_track(self, id):
        tracks = {}
        for artist in self.get_artists():
            tracks |= artist.tracks
        return tracks.get(id)

    def get_tracks(self):
        tracks = []
        for artist in self.get_artists():
            tracks += artist.tracks.values()
        return tracks

    def get_tracks_by_album(self, id):
        return self.get_album(id).tracks.values()
    
    def get_tracks_by_artist(self, id):
        return self.get_artist(id).tracks.values()
    
    def get_tracks_by_genre(self, id):
        return self.get_genre(id).tracks.values()

    def add_track(self, track):
        track.album.add_track(track)
        track.artist.add_track(track)
        for genre in track.genres:
            genre.add_track(track)

    # Albums __________________________________________________________________
    
    def get_album(self, id:int):
        return self.__albums.get(id)

    def get_albums(self):
        return self.__albums.values()

    def add_album(self, album):
        self.__albums[album.id] = album


    # Artists _________________________________________________________________

    def get_artist(self, id):
        return self.__artists.get(id)

    def get_artists(self):
        return self.__artists.values()

    def add_artist(self, artist):
        self.__artists[artist.id] = artist


    # Genres __________________________________________________________________

    def get_genre(self, id):
        return self.__genres.get(id)

    def get_genres(self):
        return self.__genres.values()

    def add_genre(self, genre):
        self.__genres[genre.id] = genre


    # Users ___________________________________________________________________

    def get_user(self, username):
        return next((user for user in self.get_users() if user.username == username), None)

    def get_users(self):
        return self.__users

    def add_user(self, user):
        self.__users.append(user)


    # Reviews _________________________________________________________________

    def get_review(self, track, user):
        try:
            return [review for review in track.reviews and user.reviews][0]
        except:
            return None

    def get_reviews(self):
        reviews = []
        for track in self.get_tracks():
            reviews += track.reviews
        return reviews

    def get_reviews_by_track(self, id):
        return self.get_track(id).reviews

    def add_review(self, review):
        review.track.add_review(review)
        review.user.add_review(review)
