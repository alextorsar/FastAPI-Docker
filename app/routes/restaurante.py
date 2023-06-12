from typing import Union

from bson import ObjectId
from fastapi import APIRouter

from app.bd import FactoriaSQL
from app.bd import FactoriaMongo
from app.routes.usuario import get_Users_With_X_Reviews
from app.schemas.restaurante import restaurantesAlgoritmoEntity, \
    restaurantesEntitySQL, restauranteEntitySQL, transformarEsquemaRelacionalAMongo
from app.models.restaurante import RestauranteMongo, RestauranteSQL

restaurante = APIRouter(
    tags=["Restaurantes"]
)


def get_Unico_Restaurante(id):
    conn = FactoriaSQL.getConexion()
    consulta = "SELECT idrestaurante, localizacion, latitud, longitud, nombre, foto_URL, place_id, price_level, " \
               "num_reviews, rating FROM bd_relacional.restaurante WHERE idrestaurante =  '{}'".format(id)
    cursor = conn.cursor()
    cursor.execute(consulta)
    results = cursor.fetchone()
    restauranteResultado = restauranteEntitySQL(results)
    conn.commit()
    conn.close()
    return restauranteResultado


def get_Todos_Restaurantes():
    conn = FactoriaSQL.getConexion()
    consulta = "SELECT idrestaurante, localizacion, latitud, longitud, nombre, foto_URL, place_id, price_level, " \
               "num_reviews, rating FROM bd_relacional.restaurante"
    cursor = conn.cursor()
    cursor.execute(consulta)
    results = cursor.fetchall()
    restaurantesRecomendados = restaurantesEntitySQL(results)
    conn.commit()
    conn.close()
    return restaurantesRecomendados


@restaurante.get("/restaurantes/")
def get_Restaurante(id: Union[str, None] = None):
    if id is not None:
        return get_Unico_Restaurante(id)
    else:
        return get_Todos_Restaurantes()


@restaurante.get("/restaurantes_Algoritmo/")
def get_Restaurantes_Algoritmo():
    conn = FactoriaMongo.getConexion()
    db = conn["tfg"]
    restaurantes = db["restaurants"]
    results = restaurantes.find()
    results = restaurantesAlgoritmoEntity(results)
    conn.close()
    return results


@restaurante.get("/restaurantes/{idUsuario}")
def get_RestaurantesRecomendados(idUsuario):
    connSQL = FactoriaSQL.getConexion()
    consulta = "SELECT indiceRecomendacion, idrestaurante, localizacion, latitud, longitud, nombre, foto_URL, " \
               "place_id, price_level, num_reviews, rating FROM bd_relacional.esrecomendadovecinoscercanos INNER JOIN " \
               "bd_relacional.restaurante ON bd_relacional.esrecomendadovecinoscercanos.restaurante_idrestaurante = " \
               "bd_relacional.restaurante.idrestaurante WHERE esrecomendadovecinoscercanos.usuario_idUsuario = '{" \
               "}'ORDER BY indiceRecomendacion DESC LIMIT 10;".format(
        idUsuario)
    cursor = connSQL.cursor()
    cursor.execute(consulta)
    results = cursor.fetchall()
    restaurantesRecomendados = restaurantesEntitySQL(results)
    connSQL.commit()
    connSQL.close()
    return restaurantesRecomendados


# FALLA
@restaurante.post("/restaurantes")
def create_Restaurante(restaurant: RestauranteSQL):
    connSQL = FactoriaSQL.getConexion()
    sentenciaSQL = "INSERT INTO bd_relacional.restaurante VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    cursor = connSQL.cursor()
    cursor.execute(sentenciaSQL, (restaurant["idrestaurante"], restaurant["localizacion"], restaurant["nombre"],
                                  restaurant["descripcion"], restaurant["latitud"], restaurant["longitud"],
                                  restaurant["foto_URL"], restaurant["place_id"],
                                  restaurant["price_level"], restaurant["rating"], restaurant["num_reviews"]))
    connSQL.commit()
    connSQL.close()
    connMongo = FactoriaMongo.getConexion()
    db = connMongo["tfg"]
    restaurants = db["restaurants"]
    restaurants.insert_one(transformarEsquemaRelacionalAMongo(restaurant))
    connMongo.close()
    return "Restaurante creado"


@restaurante.get("/algoritmo/restaurantes/{count}")
def get_RestaurantsId_From_Reviewers(count):
    conn = FactoriaMongo.getConexion()
    db = conn["tfg"]
    reviews = db["reviews"]
    usuariosXReviews = get_Users_With_X_Reviews(count)
    listaIds = []
    for i in range(len(usuariosXReviews)):
        listaIds.append(ObjectId(usuariosXReviews[i]["oid"]))

    results = reviews.find(
        {"userOid": {"$in": listaIds}},
        {"restaurantOid": 1, "_id": 0}
    )
    results = restaurantesAlgoritmoEntity(results)
    conn.close()
    return results


@restaurante.post("/restaurantes/favoritos/{idRestaurante}/{idUsuario}")
def aniadir_restaurante_favorito(idRestaurante, idUsuario):
    conn = FactoriaSQL.getConexion()
    sentencia = "INSERT INTO bd_relacional.esfavorito VALUES(%s,%s)"
    cursor = conn.cursor()
    cursor.execute(sentencia, (idUsuario,idRestaurante))
    conn.commit()
    conn.close()
    return "Aniadido a favoritos"


@restaurante.delete("/restaurantes/favoritos/delete/{idRestaurante}/{idUsuario}")
def borrar_restaurante_favorito(idRestaurante, idUsuario):
    conn = FactoriaSQL.getConexion()
    sentencia = "DELETE FROM bd_relacional.esfavorito WHERE usuario_idUsuario = %s AND restaurante_idrestaurante = %s"
    cursor = conn.cursor()
    cursor.execute(sentencia, (idUsuario,idRestaurante))
    conn.commit()
    conn.close()
    return "Borrado con exito"


@restaurante.get("/restaurantes/favoritos/{idUsuario}")
def get_restaurantes_favoritos(idUsuario):
    conn = FactoriaSQL.getConexion()
    sentencia = "SELECT idrestaurante, localizacion, latitud, longitud, nombre, foto_URL, place_id, price_level, " \
                "num_reviews, rating FROM bd_relacional.restaurante INNER JOIN bd_relacional.esfavorito ON " \
                "bd_relacional.restaurante.idrestaurante = bd_relacional.esfavorito.restaurante_idrestaurante WHERE " \
                "bd_relacional.esfavorito.usuario_idUsuario = %s"
    cursor = conn.cursor()
    cursor.execute(sentencia, idUsuario)
    results = cursor.fetchall()
    conn.commit()
    restauranteFavoritos = restaurantesEntitySQL(results)
    conn.close()
    return restauranteFavoritos


@restaurante.get("/restaurantes/favoritos/aleatorio/{idUsuario}")
def get_restaurantes_favoritos_aleatorio(idUsuario):
    conn = FactoriaSQL.getConexion()
    sentencia = "SELECT idrestaurante, localizacion, latitud, longitud, nombre, foto_URL, place_id, price_level, " \
                "num_reviews, rating FROM bd_relacional.restaurante INNER JOIN bd_relacional.esfavorito ON " \
                "bd_relacional.restaurante.idrestaurante = bd_relacional.esfavorito.restaurante_idrestaurante WHERE " \
                "bd_relacional.esfavorito.usuario_idUsuario = %s ORDER BY rand() LIMIT 1;"
    cursor = conn.cursor()
    cursor.execute(sentencia, idUsuario)
    results = cursor.fetchone()
    restauranteFavoritos = restauranteEntitySQL(results)
    conn.commit()
    conn.close()
    return restauranteFavoritos


@restaurante.get("/restaurantes/similares/{idRestaurante}")
def get_restaurantes_similares(idRestaurante):
    conn = FactoriaSQL.getConexion()
    sentencia = "SELECT idrestaurante, localizacion, latitud, longitud, nombre, foto_URL, place_id, price_level, " \
                "num_reviews, rating FROM bd_relacional.restaurante INNER JOIN bd_relacional.similitudrestaurantes ON " \
                "bd_relacional.restaurante.idrestaurante = bd_relacional.similitudrestaurantes.restaurante2 WHERE " \
                "bd_relacional.similitudrestaurantes.restaurante1 = %s AND " \
                "bd_relacional.similitudrestaurantes.restaurante1 != bd_relacional.similitudrestaurantes.restaurante2 " \
                "ORDER BY bd_relacional.similitudrestaurantes.similitud LIMIT 10"
    cursor = conn.cursor()
    cursor.execute(sentencia, idRestaurante)
    results = cursor.fetchall()
    restaurantesSimilares = restaurantesEntitySQL(results)
    conn.commit()
    conn.close()
    return restaurantesSimilares


@restaurante.get("/restaurantes/search/{restaurantName}")
def get_Restaurante_Search(restaurantName):
    conn = FactoriaSQL.getConexion()
    consulta = "SELECT idrestaurante, localizacion, latitud, longitud, nombre, foto_URL, place_id, price_level, " \
               "num_reviews, rating FROM bd_relacional.restaurante WHERE nombre REGEXP %s"
    cursor = conn.cursor()
    cursor.execute(consulta, restaurantName)
    results = cursor.fetchall()
    restaurantes = restaurantesEntitySQL(results)
    conn.commit()
    conn.close()
    return restaurantes
