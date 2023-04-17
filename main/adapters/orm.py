# main/adapters/orm.py  ______________________________________________________
# Author: Sun Lee, Mathias Sackey


from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import mapper, relationship

from main.models.else_models import Album, Artist, Genre
from main.models.msac_models import User, Review
from main.models.model import Track


metadata = MetaData()

tracks = Table(
    'tracks', metadata,
    Column('id',        Integer,        primary_key=True),
    Column('name',      String(255),    nullable=False),
    Column('url',       String(255),    nullable=False),
    Column('img_url',   String(255),    nullable=False),
    Column('time',      String(71),     nullable=False),
    Column('artist_id', ForeignKey('artists.id')),
    Column('album_id',  ForeignKey('albums.id'))
)

albums = Table(
    'albums', metadata,
    Column('id',        Integer,        primary_key=True),
    Column('name',      String(255),    nullable=False),
    Column('img_url',   String(255),    nullable=False)
)

artists = Table(
    'artists', metadata,
    Column('id',        Integer,        primary_key=True),
    Column('name',      String(255),    nullable=False),
    Column('img_url',   String(255),    nullable=False)
)

tracks_genres = Table(
    'tracks_genres', metadata,
    Column('id',        Integer,        primary_key=True),
    Column('track_id',  ForeignKey('tracks.id')),
    Column('genre_id',  ForeignKey('genres.id'))
)

genres = Table(
    'genres', metadata,
    Column('id',        Integer,        primary_key=True),
    Column('name',      String(255),    nullable=False),
    Column('img_url',   String(255),    nullable=False)
)

users = Table(
    'users', metadata, 
    Column('id',        Integer,        primary_key=True),
    Column('username',  String(255),    nullable=False, unique = True),
    Column('password',  String(255),    nullable=False)
)

reviews = Table(
    'reviews', metadata, 
    Column('id',        Integer,        primary_key=True),
    Column('datetime',  String(255),    nullable=False),
    Column('rating',    String(63),     nullable=False),
    Column('review',    String(1023),   nullable=False),
    Column('track_id',  ForeignKey('tracks.id')),
    Column('user_id',   ForeignKey('users.id'))
)


def create_mappers():

    mapper(Track, tracks, properties={
        'time':     tracks.c.time,
        'genres':   relationship(Genre,
                                secondary=tracks_genres,
                                back_populates='tracks'),
        '_Track__reviews':  relationship(Review,
                                        backref='_Review__track')
    })

    mapper(Album, albums, properties={
        'tracks':   relationship(Track,
                                backref='_Track__album')
    })

    mapper(Artist, artists, properties={
        'tracks':   relationship(Track,
                                backref='_Track__artist')
    })

    mapper(Genre, genres, properties={
        'tracks':   relationship(Track,
                                secondary=tracks_genres,
                                back_populates='genres')
    })

    mapper(User, users, properties={
        '_User__username':  users.c.username,
        '_User__password':  users.c.password,
        '_User__reviews':   relationship(Review,
                                        backref='_Review__user')
    })

    mapper(Review, reviews, properties={
        '_Review__datetime':    reviews.c.datetime,
        '_Review__rating':      reviews.c.rating,
        '_Review__review':      reviews.c.review
    })
