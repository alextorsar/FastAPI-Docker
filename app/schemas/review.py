from bson import ObjectId

from app.models.review import ReviewMongo


def reviewEntity(item) -> dict:
    if(item["restaurantName"] != None):
        restaurantName = item["restaurantName"]
    else:
        restaurantName = ""
    if (item["name"]!= None):
        name = item["name"]
    else:
        name = ""
    if (item["likesCount"]!= None):
        likesCount = item["likesCount"]
    else:
        likesCount = 0
    if (item["isLocalGuide"]!= None):
        isLocalGuide = item["isLocalGuide"]
    else:
        isLocalGuide = False
    return {
        "oid": str(item["_id"]),
        "placeId": item["placeId"],
        "restaurantName": restaurantName,
        "name": name,
        "text": item["text"],
        "likesCount": likesCount,
        "reviewId": str(item["_id"]),
        "reviewerId": item["reviewerId"],
        "reviewerUrl": "",
        "reviewerNumberOfReviews": 0,
        "isLocalGuide": isLocalGuide,
        "stars": item["stars"],
        "lastReview": item["lastReview"],
        "restaurantOid": str(item["restaurantOid"]),
        "userOid": str(item["userOid"]),
    "publishedAtDate": str(item["publishedAtDate"])
    }


def reviewsEntity(reviews) -> dict:
    return [reviewEntity(item) for item in reviews]


def reviewAlgoritmoEntity(item) -> dict:
    return {
        "stars": item["stars"],
        "userOid": str(item["userOid"]),
        "restaurantOid": str(item["restaurantOid"]),
        "idUsuario": item["idArtificialUsuario"],
        "idRestaurante": item["idArtificialRestaurante"]
    }


def reviewsAlgoritmoEntity(reviews) -> list:
    result = list()
    for review in reviews:
        result.append(reviewAlgoritmoEntity(review))

    return result

def ReviewMongoEntity(review : ReviewMongo) -> dict:
    return {
        "placeId": review.restaurantOid,
        "text": review.text,
        "reviewerId": review.userOid,
        "stars": review.stars,
        "lastReview": True,
        "userOid": ObjectId(review.userOid),
        "restaurantOid": ObjectId(review.restaurantOid),
        "publishedAtDate": review.publishedAtDate
    }


def convertReviewMongoToSQL(review: ReviewMongo, idReview):
    return{
        "idreseña": str,
        "puntuacion": int,
        "texto": str,
        "usuario_idUsuario": str,
        "restaurante_idrestaurante": str,
        "localguide": False
    }