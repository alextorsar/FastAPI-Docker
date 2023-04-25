from typing import Union

from bson import ObjectId
from fastapi import APIRouter

from app.bd import FactoriaSQL
from app.bd import FactoriaMongo
from app.routes.usuario import get_Users_With_X_Reviews
from app.schemas.restaurante import restauranteEntityMongo, restaurantesEntityMongo, restaurantesAlgoritmoEntity, \
    restaurantesEntitySQL, restauranteEntitySQL, transformarEsquemaRelacionalAMongo
from app.models.restaurante import RestauranteMongo, RestauranteSQL

router = APIRouter(
tags=["Restaurantes"]
)


def get_Unico_Restaurante(id):
    conn = FactoriaSQL.getConexion();
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
    conn = FactoriaSQL.getConexion();
    consulta = "SELECT idrestaurante, localizacion, latitud, longitud, nombre, foto_URL, place_id, price_level, " \
               "num_reviews, rating FROM bd_relacional.restaurante"
    cursor = conn.cursor()
    cursor.execute(consulta)
    results = cursor.fetchall()
    restaurantesRecomendados = restaurantesEntitySQL(results)
    conn.commit()
    conn.close()
    return restaurantesRecomendados


@router.get("/restaurantes/")
def get_Restaurante(id: Union[str, None] = None):
    if id is not None:
        return get_Unico_Restaurante(id)
    else:
        return get_Todos_Restaurantes()


@router.get("/restaurantes/{idUsuario}")
def get_RestaurantesRecomendados(idUsuario):
    conn = FactoriaSQL.getConexion();
    consulta = "SELECT indiceRecomendacion, idrestaurante, localizacion, latitud, longitud, nombre, foto_URL, place_id, price_level, num_reviews, rating FROM bd_relacional.esrecomendadovecinoscercanos INNER JOIN bd_relacional.restaurante ON bd_relacional.esrecomendadovecinoscercanos.restaurante_idrestaurante = bd_relacional.restaurante.idrestaurante WHERE esrecomendadovecinoscercanos.usuario_idUsuario = '{}'ORDER BY indiceRecomendacion DESC LIMIT 10;".format(
        idUsuario)
    cursor = conn.cursor()
    cursor.execute(consulta)
    results = cursor.fetchall()
    restaurantesRecomendados = restaurantesEntitySQL(results)
    conn.commit()
    conn.close()
    return restaurantesRecomendados


@router.post("/restaurantes")
def create_Restaurante(restaurant: RestauranteSQL):
    connSQL = FactoriaSQL.getConexion()
    sentenciaSQL = "INSERT INTO restaurante VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
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


@router.get("/reviews/restaurantes/{count}")
def get_RestaurantsId_From_Reviewers(count):
    conn = FactoriaMongo.getConexion()
    db = conn["tfg"]
    reviews = db["reviews"]
    usuariosXReviews = get_Users_With_X_Reviews(count)

    listaIds = []
    for i in range(len(usuariosXReviews)):
        print(i)
        listaIds.append(ObjectId(usuariosXReviews[i]["oid"]))

    results = reviews.find(
        {"userOid": {"$in": listaIds}},
        {"restaurantOid": 1, "_id": 0}
    )
    conn.close()
    return restaurantesAlgoritmoEntity(results)
