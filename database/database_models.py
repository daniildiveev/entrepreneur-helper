from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sa

Base = declarative_base()

class Request(Base):
    __tablename__ = 'requests'

    user_id = sa.Column(sa.INTEGER, foreign_key=True)
    request_id = sa.Column(sa.INTEGER, primary_key=True)
    time = sa.Column(sa.DATETIME)
    query = sa.Column(sa.TEXT)

class User(Base):
    __tablename__ = 'users'

    user_id = sa.Column(sa.INTEGER, primary_key=True)
    times_used_before = sa.Column(sa.INTEGER)
