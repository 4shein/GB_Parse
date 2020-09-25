from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import DateTime
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Table
)

BASE = declarative_base()

"""
one to many - один к многому
many to one - многое к одному
one to one - один к одному
many to many - многое к многому
"""

tag_post = Table('tag_post', BASE.metadata,
                 Column('post_id', Integer, ForeignKey('post.id')),
                 Column('tag_id', Integer, ForeignKey('tag.id'))
                 )


class Post(BASE):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False, unique=False)
    url = Column(String, nullable=False, unique=True)
    writer_id = Column(Integer, ForeignKey('writer.id'), nullable=False)
    writer = relationship("Writer", back_populates='post')
    tags = relationship('Tag', secondary=tag_post, back_populates='posts')
    image_url = Column(String, nullable=False, unique=False)
    pub_date = Column(DateTime, nullable=False, unique=False)


    def __init__(self, title, url, writer, tags, image_url, pub_date):
        tags = tags if tags else []
        self.title = title
        self.url = url
        self.writer = writer
        self.tags.extend(tags)
        self.image_url = image_url
        self.pub_date = pub_date


class Writer(BASE):
    __tablename__ = 'writer'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=False)
    url = Column(String, nullable=False, unique=True)
    post = relationship('Post', back_populates='writer')

    def __init__(self, name, url):
        self.name = name
        self.url = url


class Tag(BASE):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    url = Column(String, nullable=False, unique=True)
    posts = relationship('Post', secondary=tag_post, back_populates='tags')

    def __init__(self, name, url):
        self.name = name
        self.url = url

