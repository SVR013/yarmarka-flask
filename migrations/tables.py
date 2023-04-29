from sqlalchemy import create_engine, MetaData, Table, String, Integer, Column, Text, DateTime, Boolean
from datetime import datetime
from math import floor
import time as t
###
from sqlalchemy import create_engine, MetaData, Table, Integer, String, \
    Column, DateTime, ForeignKey, Numeric
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

from sqlalchemy import MetaData, Table, Integer, String, Column, Text, DateTime, Boolean
from sqlalchemy.orm import registry
from datetime import datetime

__ENGINE__ = create_engine('sqlite:////home//funeralclown/yarmarka/migrations/yarmarka.db')
__BASE__ = declarative_base()
__METADATA__ = MetaData()


class MainPageT(__BASE__):
    __tablename__ = 'main_page'
    id = Column(Integer(), primary_key=True)

    head = Column(Text())
    date = Column(Text())
    place = Column(Text())
    time = Column(Text())
    phone = Column(Text())

    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)


class FeedbackT(__BASE__):
    __tablename__ = 'feedback'
    id = Column(Integer(), primary_key=True)

    email = Column(Text())
    number = Column(Text())
    comment = Column(Text())
    time = Column(Integer(), default=floor(t.time()), onupdate=floor(t.time()))


class MembersT(__BASE__):
    __tablename__ = 'members'
    id = Column(Integer(), primary_key=True)

    pavilion = Column(Text(), nullable=False, unique=True)
    title = Column(Text())
    text = Column(Text())
    time = Column(Integer(), default=floor(t.time()), onupdate=floor(t.time()))
    img = Column(Text())
    date = Column(Text(), default=t.strftime('%d.%m.%Y %H:%M', t.localtime(t.time())),
                  onupdate=t.strftime('%d.%m.%Y %H:%M', t.localtime(t.time())))


class PostsT(__BASE__):
    __tablename__ = 'posts'
    id = Column(Integer(), primary_key=True)

    url = Column(Text(), nullable=False, unique=True)
    title = Column(Text())
    text = Column(Text())
    time = Column(Integer(), default=floor(t.time()), onupdate=floor(t.time()))
    img = Column(Text())
    date = Column(Text(), default=t.strftime('%d.%m.%Y %H:%M', t.localtime(t.time())),
                  onupdate=t.strftime('%d.%m.%Y %H:%M', t.localtime(t.time())))


class UsersT(__BASE__):
    __tablename__ = 'users'
    id = Column(Integer(), primary_key=True)
    user = Column(Text(), nullable=False)
    psw = Column(Text(), nullable=False)


__BASE__.metadata.create_all(__ENGINE__)
