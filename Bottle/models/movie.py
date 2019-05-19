
from sqlalchemy import Column, Integer, String, SmallInteger, DECIMAL

from Bottle.models.base import BaseModel, db


class MovieModel(BaseModel):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50))
    score = Column(String(10))
    cover = Column(String(100))
    url = Column(String(100))
    movieId = Column(Integer)

    def keys(self):
        return ['movieId', 'title', 'score', 'cover', 'url']


class HotMovie(MovieModel):
    __tablename__ = 'hot_movie'

class NewMovie(MovieModel):
    __tablename__ = 'new_movie'

class ClassicMovie(MovieModel):
    __tablename__ = 'classic_movie'