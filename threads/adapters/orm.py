from sqlalchemy import Table, MetaData, Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import mapper, relationship
from threads.domainmodel.model import Tag, User, Review, Thread, Favorite

metadata = MetaData()

tags = Table(
    'tags', metadata,
    Column('tag_name', String(255), primary_key=True)
)

threads = Table(
    'threads', metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String(255), nullable=False),
    Column('release_date', String(255), nullable=True),
    Column('description', Text, nullable=True),
    Column('user_id', Integer, ForeignKey('users.id'))  # Foreign key to users
)

thread_tags = Table(
    'thread_tags', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('thread_id', Integer, ForeignKey('threads.id')),
    Column('tag_name', String(255), ForeignKey('tags.tag_name'))
)

users = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('username', String(255), nullable=False, unique=True),
    Column('password', String(255), nullable=False),
    Column('email', String(255), nullable=True),
    Column('dob', String(255), nullable=True),
    Column('gender', String(255), nullable=True),
)

reviews = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('thread_id', Integer, ForeignKey('threads.id')),
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('rating', Integer, nullable=False),
    Column('comment', Text, nullable=True)
)

favorites = Table(
    'favorites', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', Integer, ForeignKey('users.id')),
)

favorite_threads = Table(
    'favorite_threads', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('favorite_id', Integer, ForeignKey('favorites.id')),
    Column('thread_id', Integer, ForeignKey('threads.id'))
)

from sqlalchemy.orm import mapper, relationship
from threads.domainmodel.model import Tag, User, Review, Thread, Favorite

def map_model_to_tables():
    # Tag mapping
    mapper(Tag, tags, properties={
        'tag_name': tags.c.tag_name,
        'threads': relationship(Thread, secondary=thread_tags, back_populates='tags')
    })

    # Thread mapping
    mapper(Thread, threads, properties={
        'thread_title': threads.c.title,
        'release_date': threads.c.release_date,
        'description': threads.c.description,
        'tags': relationship(Tag, secondary=thread_tags, back_populates='threads'),
        'reviews': relationship(Review, back_populates='thread'),
        'user': relationship(User, back_populates='threads', uselist=False)
    })

    # User mapping
    mapper(User, users, properties={
        'username': users.c.username,
        'password': users.c.password,
        'email': users.c.email,
        'dob': users.c.dob,
        'gender': users.c.gender,
        'threads': relationship(Thread, back_populates='user'),
        'reviews': relationship(Review, back_populates='user'),
        'favorite': relationship(Favorite, uselist=False, back_populates='user')
    })

    # Review mapping
    mapper(Review, reviews, properties={
        'rating': reviews.c.rating,
        'comment': reviews.c.comment,
        'user': relationship(User, back_populates='reviews'),
        'thread': relationship(Thread, back_populates='reviews')
    })

    # Favorite mapping
    mapper(Favorite, favorites, properties={
        'user': relationship(User, back_populates='favorite'),
        'list_of_threads': relationship(Thread, secondary=favorite_threads)
    })
