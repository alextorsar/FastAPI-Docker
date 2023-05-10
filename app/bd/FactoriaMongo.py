from pymongo import MongoClient

import app.utils.db as db


def getConexion():
    return MongoClient(db.URL_MONGO)
