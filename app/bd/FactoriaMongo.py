from pymongo import MongoClient

import config.db as db


def getConexion():
    return MongoClient(db.URL_MONGO)