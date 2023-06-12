from app.models.usuario import UsuarioSQL, UsuarioMongo


def usuarioAlgoritmoEntity(item, idArtifical) -> dict:
    return {
        "oid": str(item["_id"]),
        "idArtificial": idArtifical
    }


def usuariosAlgoritmoEntity(usuarios) -> list:
    result = list()
    idArtificial = 1
    for usuario in usuarios:
        result.append(usuarioAlgoritmoEntity(usuario, idArtificial))
        idArtificial = idArtificial + 1
    return result


def usuarioEntity(item) -> dict:
    return {
        "oid": str(item["_id"]),
        "name": item["name"],
        "reviewerId": item["reviewerId"],
        "reviewerUrl": item["reviewerUrl"],
        "reviewerNumberOfReviews": item["reviewerNumberOfReviews"],
        "isLocalGuide": item["isLocalGuide"],
        "numReviewsEnBD": item["numReviewsEnBD"],
    }


def usuariosEntity(usuarios) -> list:
    return [usuarioEntity(item) for item in usuarios]


def usuarioEntityId(item) -> dict:
    return {
        "oid": str(item["_id"])
    }


def usuariosEntityId(usuarios) -> list:
    return [usuarioEntityId(item) for item in usuarios]


def usuarioEntitySQL(item) -> dict:
    return {
        "oid": item["idUsuario"],
        "idArtificial": item["idArtificial"]
    }


def usuariosEntitySQL(usuarios) -> list:
    return [usuarioEntitySQL(item) for item in usuarios]


def convertUserSQLToMongo(usuario: UsuarioSQL):
    return {
        "name": usuario.Nombre,
        "reviewerId": None,
        "reviewerUrl": None,
        "reviewerNumberOfReviews": 0,
        "isLocalGuide": False,
        "numReviewsEnBD": 0
    }
