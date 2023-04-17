# main/browse/services.py _____________________________________________________
# Author: Sun Lee, Mathias Sackey


from main.adapters.abstract_repository import repo as repo
from main.adapters.services import write_reviews
from main.models.msac_models import Review


def get_alphanumeric(tag, i):
    alphanumeric = []
    if not i.isdigit():
        alphanumeric = [attr.name[0].lower() for attr in getattr(repo, f'get_{tag}s')()
                        if 96 < ord(attr.name[0].lower()) < 123] + ['#']

    return sorted(set(alphanumeric))

def get_track(id):
    return repo.get_track(id)


def get_tag(tag, i):
    # return album/artist/genre name
    if i.isdigit():
        return getattr(repo, f'get_{tag}')(int(i)).name
    
    # return Album/Artist/Genre
    return tag


def get_tagged(tag, i):
    # return tracks
    if i.isdigit():
        return getattr(repo, f'get_tracks_by_{tag}')(int(i))
    
    # return albums/artists/genres
    else:

        # non-alphabetical
        if i == '#':
            return [attr for attr in getattr(repo, f'get_{tag}s')()
                    if not (96 < ord(attr.name[0].lower()) < 123)]
        
        # alphabetical
        else:
            return [attr for attr in getattr(repo, f'get_{tag}s')()
                    if attr.name[0].lower() == i]


def add_review(track_id, user_name, datetime, rating, review):
    track = repo.get_track(track_id)
    user =  repo.get_user(user_name)
    r = repo.get_review(track, user)
    # remove old review
    if r:
        track.remove_review(r)
        user.remove_review(r)
    # add new review
    r = Review(datetime, rating, review, track, user)
    repo.add_review(r)
    write_reviews(repo)
