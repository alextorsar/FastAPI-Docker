def findIdArtificialUsuarioMongo(review, usuariosXReviews):
    idBuscado = str(review["userOid"])
    encontrado = False
    i = 0
    while not encontrado:
        if idBuscado == usuariosXReviews[i]["oid"]:
            result = usuariosXReviews[i]["idArtificial"]
            encontrado = True
        i = i+1
    return result


def findIdArtificialRestauranteMongo(review, restaurantesXReviews):
    idBuscado = str(review["restaurantOid"])
    encontrado = False
    i = 0
    while not encontrado:
        if idBuscado == restaurantesXReviews[i]["oid"]:
            result = restaurantesXReviews[i]["id"]
            encontrado = True
        i = i+1
    return result


def findIdArtificialUsuarioSQL(usuario, usuariosXReviews):
    idBuscado = usuario["idUsuario"]
    encontrado = False
    i = 0
    while not encontrado:
        if idBuscado == usuariosXReviews[i]["oid"]:
            result = usuariosXReviews[i]["idArtificial"]
            encontrado = True
        i = i+1
    return result
