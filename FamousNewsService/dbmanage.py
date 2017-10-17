import os
from models import base
from sqlalchemy import create_engine


def create_db():
    db = create_engine(os.environ.get("COMMANDDB_HOST"))
    base.metadata.create_all(db)


def create_dev_db():
    db = create_engine(os.environ.get("COMMANDDB_DEV_HOST"))
    base.metadata.create_all(db)


def create_test_db():
    db = create_engine(os.environ.get("COMMANDDB_TEST_HOST"))
    base.metadata.create_all(db)


if __name__ == '__main__':
    print('creating databases')
    create_db()
    create_dev_db()
    create_test_db()
    print('databases created')
