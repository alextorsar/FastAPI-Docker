from bson.objectid import ObjectId
from fastapi import APIRouter
from app.bd import FactoriaMongo, FactoriaSQL
from app.schemas.usuario import usuarioEntity, usuariosEntity, usuariosAlgoritmoEntity, usuariosEntitySQL
from app.models.usuario import UsuarioMongo
from app.utils.utils import findIdArtificialUsuarioSQL

usuario = APIRouter(
    tags=["Usuarios"]
)


@usuario.get("/usuarios")
def get_Usuarios():
    conn = FactoriaMongo.getConexion()
    db = conn["tfg"]
    coll = db["users"]
    result = coll.find({})
    conn.close()
    return usuariosEntity(result)


@usuario.get("/usuarios/{id}")
def get_Usuario(id):
    conn = FactoriaMongo.getConexion()
    db = conn["tfg"]
    coll = db["users"]
    usuario_bd = usuarioEntity(coll.find_one({"_id": ObjectId(id)}))
    conn.close()
    return dict(usuario_bd)


@usuario.post("/usuarios")
def create_Usuarios(user: UsuarioMongo):
    conn = FactoriaMongo.getConexion()
    db = conn["tfg"]
    coll = db["users"]
    nuevo_usuario = dict(user)
    coll.insert_one(nuevo_usuario)
    conn.close()
    return "Usuario creado"


@usuario.put("/usuarios/{id}")
def put_Usuario(id: str, user: UsuarioMongo):
    conn = FactoriaMongo.getConexion()
    db = conn["tfg"]
    coll = db["users"]
    result = coll.find_one_and_update(
        {"_id": ObjectId(id)},
        {{"$set": dict(user)}}
    )
    conn.close()
    return result


@usuario.delete("/usuarios/{id}")
def delete_Usuario(id):
    conn = FactoriaMongo.getConexion()
    db = conn["tfg"]
    coll = db["users"]
    myquery = {"_id": ObjectId(id)}
    coll.delete_one(myquery)
    conn.close()
    return "Usuario Borrado con éxito"

@usuario.get("/usuarios/usersWithReviews/{count}")
def get_Users_With_X_Reviews(count):
    conn = FactoriaMongo.getConexion()
    db = conn["tfg"]
    coll = db["users"]
    usuarios = coll.find(
        {"numReviewsEnBD": {"$gte": int(count)}}
    )
    result = usuariosEntity(usuarios)
    conn.close()
    return result


@usuario.get("/algoritmo/usuarios/{count]")
def get_Users_With_X_Reviews_Algorythm(count):
    conn = FactoriaMongo.getConexion()
    db = conn["tfg"]
    coll = db["users"]
    usuarios = coll.find(
        {"numReviewsEnBD": {"$gte": int(count)}},
        {"_id": 1}
    )
    result = usuariosAlgoritmoEntity(usuarios)
    conn.close()
    return result


@usuario.get("/algoritmo/usuarios/operacionales/{count]")
def get_Operational_Users_With_X_Reviews_Algorythm(count):
    conn = FactoriaSQL.getConexion()
    consulta = "SELECT idUsuario FROM bd_relacional.usuario INNER JOIN bd_relacional.reseña ON bd_relacional.usuario.idUsuario = bd_relacional.reseña.usuario_idUsuario GROUP " \
               "BY bd_relacional.usuario.idUsuario HAVING COUNT(*) >= " + count
    cursor = conn.cursor()
    cursor.execute(consulta)
    users = cursor.fetchall()

    usuariosXReviews = get_Users_With_X_Reviews_Algorythm(count)
    results = []
    for user in users:
        user["idArtificial"] = findIdArtificialUsuarioSQL(user, usuariosXReviews)
        results.append(user)

    users = usuariosEntitySQL(results)

    conn.commit()
    conn.close()
    return users
