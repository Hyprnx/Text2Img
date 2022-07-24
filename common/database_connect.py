import logging

from pymongo import MongoClient
from pymongo.database import Database
from configparser import ConfigParser


def connect_to_database(path='config.ini', profile='local'):
    try:
        config = ConfigParser()
        config.read_file(open(path))
        host = config.get(profile, 'host')
        port = config.getint(profile, 'port')
        client = MongoClient(host, port)
        db = client.database
        if not isinstance(db, Database):
            raise ConnectionError("Connection failed, respond is not a MongoDB Database instance")
        return db
    except BaseException as e:
        raise ConnectionError(f'Failed Establishing connection to database with error: \n {e}')


if __name__ == '__main__':
    db = connect_to_database()
    sample = {
        "source": "sample source",
        "title": "sample title",
        "sapo": "sample sapo",
        "body": "sample body",
        "id": 123456879,
        "publish": "2022-07-24T22:15:07Z",
        "tags": [
            "sample tags"
        ],
        "keywords": [
            "sample keyword"
        ],
        "cates": [
            "sample cates"
        ]
    }
    db['news'].insert_one(sample)
