
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from sqlalchemy import Column, Integer, Text, SmallInteger
from contextlib import contextmanager
from datetime import datetime

from Bottle.errors.error_code import NotFound


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e


class Query(BaseQuery):
    def filter_by(self, **kwargs):
        if 'status' not in kwargs.keys():
            kwargs.update(status=1)
        return super(Query, self).filter_by(**kwargs)

    def get_or_404(self, ident, description=None):
        """Like :meth:`get` but aborts with 404 if not found instead of returning ``None``."""

        rv = self.get(ident)
        if rv is None:
            raise NotFound()
        return rv

    def first_or_404(self, description=None):
        """Like :meth:`first` but aborts with 404 if not found instead of returning ``None``."""

        rv = self.first()
        if rv is None:
            raise NotFound()
        return rv


db = SQLAlchemy(query_class=Query)


class BaseModel(db.Model):
    __abstract__ = True
    create_time = Column('create_time', Integer)
    status = Column(SmallInteger, default=1)

    def __init__(self):
        self.create_time = int(datetime.now().timestamp())


    @property
    def create_datetime(self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        else:
            return None

    def delete(self):
        self.status = 0

    def __getitem__(self, item):
        return getattr(self, item)
