import os
from models import Base
from sqlalchemy import create_engine


def create_db():
    db = create_engine(os.environ.get("COMMANDDB_HOST"))
    db.execute('CREATE SEQUENCE IF NOT EXISTS news_id_seq START 1;')
    Base.metadata.create_all(db)


def create_dev_db():
    db = create_engine(os.environ.get("COMMANDDB_DEV_HOST"))
    db.execute('CREATE SEQUENCE IF NOT EXISTS news_id_seq START 1;')
    Base.metadata.create_all(db)


def create_test_db():
    db = create_engine(os.environ.get("COMMANDDB_TEST_HOST"))
    db.execute('CREATE SEQUENCE IF NOT EXISTS news_id_seq START 1;')
    Base.metadata.create_all(db)


if __name__ == '__main__':
    print('creating databases')
    create_db()
    create_dev_db()
    create_test_db()
    print('databases created')
