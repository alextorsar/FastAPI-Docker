from pymongo import MongoClient

import app.config.db as db


def getConexion():
    return MongoClient(db.URL_MONGO)
