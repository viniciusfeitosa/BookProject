import os
from datetime import datetime
from mongoengine import MongoEngine

from sqlalchemy import create_engine
from sqlalchemy import (
    Column,
    String,
    BigInteger,
    DateTime,
    Index,
)
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import UUIDType

db_string = os.environ.get('COMMAND_DEV_HOST')

db_engine = create_engine(db_string)
base = declarative_base()
Session = sessionmaker(db_engine)
session = Session()


class CommandNewsModel(base):
    __tablename__ = 'news'

    news_id = Column(UUIDType(), primary_key=True)
    news_version = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String(length=200))
    content = Column(String)
    author = Column(String(length=50))
    created_at = Column(DateTime, default=datetime.utcnow)
    published_at = Column(DateTime)
    news_type = Column(String, default='famous')
    tags = Column(postgresql.ARRAY(String))

    __table_args__ = Index('index', 'news_id', 'news_version'),


mongo_db = MongoEngine()
mongo_db.init_app(os.environ.get('QUERYBD_HOST'))


class QueryNewsModel(mongo_db.Document):
    news_version = mongo_db.IntegerField(required=True)
    title = mongo_db.StringField(required=True, max_length=200)
    content = mongo_db.StringField(required=True)
    author = mongo_db.StringField(required=True, max_length=50)
    created_at = mongo_db.DateTimeField(default=datetime.datetime.now)
    published_at = mongo_db.DateTimeField()
    news_type = mongo_db.StringField(default="famous")
    tags = mongo_db.ListField(mongo_db.StringField(max_length=50))
