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
    }


def reviewsEntity(reviews) -> dict:
    return [reviewEntity(item) for item in reviews]


def reviewAlgoritmoEntity(item, idArtificialUsuario, idArtificialRestaurante) -> dict:
    return {
        "stars": item["stars"],
        "userOid": item["userOid"],
        "restaurantOid": item["restaurantOid"],
        "idUsuario": idArtificialUsuario,
        "idRestaurante": idArtificialRestaurante
    }


def reviewsAlgoritmoEntity(reviews, usuariosXReviews, restaurentesFromReviews) -> list:
    result = list()
    for review in reviews:
        idArtificialUsuario = 0
        idArtificialRestaurante = 0
        result.append(reviewAlgoritmoEntity(review,idArtificialUsuario, idArtificialRestaurante))


    return result