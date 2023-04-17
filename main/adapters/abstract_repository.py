repo = None


class AbstractRepository:

    # Tracks __________________________________________________________________

    def get_track(self, id):
        raise NotImplementedError

    def get_tracks(self):
        raise NotImplementedError

    def get_tracks_by_album(self, id):
        raise NotImplementedError
    
    def get_tracks_by_artist(self, id):
        raise NotImplementedError
    
    def get_tracks_by_genre(self, id):
        raise NotImplementedError

    def add_track(self, track):
        raise NotImplementedError


    # Albums __________________________________________________________________
    
    def get_album(self, id):
        raise NotImplementedError

    def get_albums(self):
        raise NotImplementedError

    def add_album(self, album):
        raise NotImplementedError


    # Artists _________________________________________________________________

    def get_artist(self, id):
        raise NotImplementedError

    def get_artists(self):
        raise NotImplementedError

    def add_artist(self, artist):
        raise NotImplementedError

    
    # Genres __________________________________________________________________

    def get_genre(self, id):
        raise NotImplementedError

    def get_genres(self):
        raise NotImplementedError

    def add_genre(self, genre):
        raise NotImplementedError
    
    
    # Users ___________________________________________________________________

    def get_user(self, username):
        raise NotImplementedError

    def get_users(self):
        raise NotImplementedError

    def add_user(self, user):
        raise NotImplementedError


    # Reviews _________________________________________________________________

    def get_review(self, track, user):
        raise NotImplementedError

    def get_reviews(self):
        raise NotImplementedError

    def get_reviews_by_track(self, id):
        raise NotImplementedError

    def add_review(self, review):
        raise NotImplementedError