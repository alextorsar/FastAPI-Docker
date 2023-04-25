import config.db as db
import pymysql


def getConexion():
    connSQL = pymysql.connect(host=db.HOST,
                              port=db.PORT,
                              user=db.USER,
                              passwd=db.PASSWORD,
                              cursorclass=pymysql.cursors.DictCursor)
    return connSQL
