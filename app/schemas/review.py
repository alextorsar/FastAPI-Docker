from bson import ObjectId

from app.models.review import ReviewMongo


def reviewEntity(item) -> dict:
    return {
        "oid": str(item["_id"]),
        "placeId": item["placeId"],
        "restaurantName": item["restaurantName"],
        "name": item["name"],
        "text": item["text"],
        "publishedAtDate": item["publishedAtDate"],
        "likesCount": item["likesCount"],
        "reviewId": item["reviewId"],
        "reviewerId": item["reviewerId"],
        "reviewerUrl": item["reviewerUrl"],
        "reviewerNumberOfReviews": item["reviewerNumberOfReviews"],
        "isLocalGuide": item["isLocalGuide"],
        "stars": item["stars"],
        "lastReview": item["lastReview"],
        "restaurantOid": str(item["restaurantOid"]),
        "userOid": str(item["userOid"])
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
        "restaurantOid": ObjectId(review.restaurantOid)
    }
