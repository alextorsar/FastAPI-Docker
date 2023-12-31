import datetime
import json

from bson.objectid import ObjectId
from fastapi import APIRouter, Depends
from app.bd import FactoriaMongo
from app.bd import FactoriaSQL
from app.routes.restaurante import get_RestaurantsId_From_Reviewers
from app.schemas.review import reviewEntity, reviewsEntity, reviewsAlgoritmoEntity, ReviewMongoEntity
from app.models.review import ReviewMongo
from app.routes.usuario import get_Users_With_X_Reviews, get_Users_With_X_Reviews_Algorythm
from app.utils.utils import findIdArtificialUsuarioMongo, findIdArtificialRestauranteMongo
from app.auth.auth_bearer import JWTBearer

review = APIRouter(
    tags=["Reviews"]
)

@review.get("/reviews")
def get_Reviews():
    conn = FactoriaMongo.getConexion()
    db = conn["tfg"]
    coll = db["reviews"]
    result = coll.find({})
    conn.close()
    return reviewsEntity(result)


@review.get("/reviews/{id}", dependencies=[Depends(JWTBearer())])
def get_Review(id):
    conn = FactoriaMongo.getConexion()
    db = conn["tfg"]
    coll = db["reviews"]
    rewiew_bd = reviewEntity(coll.find_one({"_id": ObjectId(id)}))
    conn.close()
    return dict(rewiew_bd)


@review.get("/reviews/user/{id}",dependencies=[Depends(JWTBearer())])
def get_User_Reviews(id):
    conn = FactoriaMongo.getConexion()
    db = conn["tfg"]
    coll = db["reviews"]
    reviews = coll.find(
        {"userOid": ObjectId(id)}
    )
    results = reviewsEntity(reviews)
    conn.close()
    return results


@review.post("/review", dependencies=[Depends(JWTBearer())])
def create_Review(review: ReviewMongo):
    conn = FactoriaMongo.getConexion()
    db = conn["tfg"]
    coll = db["reviews"]
    review.publishedAtDate = datetime.datetime.now()
    idReview = coll.insert_one(ReviewMongoEntity(review)).inserted_id
    idReview = str(idReview)
    conn.close()
    connSQL = FactoriaSQL.getConexion()
    sentencia = "INSERT INTO bd_relacional.reseña(idreseña, puntuacion, texto, usuario_idUsuario, restaurante_idrestaurante) VALUES (%s, %s, %s, %s, %s)"
    cursor = connSQL.cursor()
    cursor.execute(sentencia, (idReview, review.stars, review.text, review.userOid, review.restaurantOid))
    connSQL.commit()
    connSQL.close()
    return "Review creada"


@review.get("/reviews/usuarios/{count}")
def get_Reviews_From_Reviewers(count):
    conn = FactoriaMongo.getConexion()
    db = conn["tfg"]
    coll = db["reviews"]
    usuariosXReviews = get_Users_With_X_Reviews(count)

    restaurentesFromReviews = get_RestaurantsId_From_Reviewers(count)

    listaIdsUsuarios = []
    for i in range(len(usuariosXReviews)):
        listaIdsUsuarios.append(ObjectId(usuariosXReviews[i]["oid"]))

    listaIdsRestaurantes = []
    for i in range(len(restaurentesFromReviews)):
        listaIdsRestaurantes.append(ObjectId(restaurentesFromReviews[i]["oid"]))

    result = coll.find(
        {"userOid": {"$in": listaIdsUsuarios}},
        {"restaurantOid": 1, "stars": 1, "userOid": 1, "_id": 0}
    )
    reviews = reviewsAlgoritmoEntity(result)
    conn.close()
    return reviews


@review.get("/reviews/restaurant/{id}")
def get_Reviews_from_Restaurant(id):
    conn = FactoriaMongo.getConexion()
    db = conn["tfg"]
    coll = db["reviews"]
    reviews = coll.find(
        {"restaurantOid": ObjectId(id)}
    ).limit(10)
    return reviewsEntity(reviews)


@review.get("/algoritmo/review/{count}")
def get_ReviewsId_From_Reviewers(count):
    conn = FactoriaMongo.getConexion()
    db = conn["tfg"]
    reviews = db["reviews"]
    usuariosXReviews = get_Users_With_X_Reviews_Algorythm(count)
    restaurantesXReviews = get_RestaurantsId_From_Reviewers(count)
    listaIds = []
    for i in range(len(usuariosXReviews)):
        listaIds.append(ObjectId(usuariosXReviews[i]["oid"]))

    reviews = reviews.find(
        {"userOid": {"$in": listaIds}},
        {"restaurantOid": 1, "_id": 0, "userOid": 1, "stars": 1}
    )
    results = []
    for review in reviews:
        review["idArtificialUsuario"] = findIdArtificialUsuarioMongo(review, usuariosXReviews)
        review["idArtificialRestaurante"] = findIdArtificialRestauranteMongo(review, restaurantesXReviews)
        results.append(review)

    reviews = reviewsAlgoritmoEntity(results)
    conn.close()
    return reviews

