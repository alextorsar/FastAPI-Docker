import json

from bson.objectid import ObjectId
from fastapi import APIRouter

from app.bd import FactoriaMongo
from app.routes.restaurante import get_RestaurantsId_From_Reviewers
from app.schemas.review import reviewEntity, reviewsEntity, reviewsAlgoritmoEntity
from app.models.review import ReviewMongo
from app.routes.usuario import get_Users_With_X_Reviews

router = APIRouter(
    tags=["Reviews"]
)

@router.get("/reviews")
def get_Reviews():
    conn = FactoriaMongo.getConexion()
    db = conn["tfg"]
    coll = db["reviews"]
    result = coll.find({})
    conn.close()
    return reviewsEntity(result)


@router.get("/reviews/{id}")
def get_Review(id):
    conn = FactoriaMongo.getConexion()
    db = conn["tfg"]
    coll = db["reviews"]
    rewiew_bd = reviewEntity(coll.find_one({"_id": ObjectId(id)}))
    conn.close()
    return dict(rewiew_bd)


@router.get("/reviews/user/{id}")
def get_User_Reviews(id):
    conn = FactoriaMongo.getConexion()
    db = conn["tfg"]
    coll = db["reviews"]
    reviews = coll.find(
        {"userOid": ObjectId(id)}
    )
    return reviewsEntity(reviews)


@router.post("/revievs")
def create_Review(review: ReviewMongo):
    conn = FactoriaMongo.getConexion()
    db = conn["tfg"]
    coll = db["reviews"]
    coll.insert_one(review.dict())
    conn.close()
    return "Review creada"


@router.get("/reviews/usuarios/{count}")
def get_Reviews_From_Reviewers(count):
    conn = FactoriaMongo.getConexion()
    db = conn["tfg"]
    coll = db["reviews"]
    usuariosXReviews = get_Users_With_X_Reviews(count)

    restaurentesFromReviews = get_RestaurantsId_From_Reviewers(count)

    listaIdsUsuarios = []
    for i in range(len(usuariosXReviews)):
        print(i)
        listaIdsUsuarios.append(ObjectId(usuariosXReviews[i]["oid"]))

    listaIdsRestaurantes = []
    for i in range(len(restaurentesFromReviews)):
        print(i)
        listaIdsRestaurantes.append(ObjectId(restaurentesFromReviews[i]["oid"]))

    result = coll.find(
        {"userOid": {"$in": listaIdsUsuarios}},
        {"restaurantOid": 1, "stars": 1, "userOid": 1, "_id": 0}
    )
    conn.close()
    return reviewsAlgoritmoEntity(result, listaIdsUsuarios, listaIdsRestaurantes)


@router.get("/reviews/restaurant/{id}")
def get_Reviews_from_Restaurant(id):
    conn = FactoriaMongo.getConexion()
    db = conn["tfg"]
    coll = db["reviews"]
    reviews = coll.find(
        {"restaurantOid": ObjectId(id)}
    )
    return reviewsEntity(reviews)
