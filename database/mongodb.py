import os

from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient


class MongoDB(object):
    load_dotenv(find_dotenv())

    @staticmethod
    def get_connection():
        return MongoClient(
            f"mongodb+srv://"
            f"{os.environ.get('MDB_USERNAME')}:"
            f"{os.environ.get('MDB_PASSWORD')}"
            f"@news-search.kpgz8.mongodb.net/News-Search?retryWrites=true&w=majority"
        )
