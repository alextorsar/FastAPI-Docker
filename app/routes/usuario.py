from bson.objectid import ObjectId
from fastapi import APIRouter, HTTPException
from app.bd import FactoriaMongo
from app.schemas.usuario import usuarioEntity, usuariosEntity, usuariosAlgoritmoEntity, usuariosEntityId
from app.models.usuario import UsuarioMongo

router = APIRouter(
tags=["Usuarios"]
)


@router.get("/usuarios")
def get_Usuarios():
    conn = FactoriaMongo.getConexion()
    db = conn["tfg"]
    coll = db["users"]
    result = coll.find({})
    conn.close()
    return usuariosEntity(result)


@router.get("/usuarios/{id}")
def get_Usuario(id):
    conn = FactoriaMongo.getConexion()
    db = conn["tfg"]
    coll = db["users"]
    usuario_bd = usuarioEntity(coll.find_one({"_id": ObjectId(id)}))
    if usuario_bd:
        return dict(usuario_bd)
    else:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")


@router.post("/usuarios")
def create_Usuarios(user: UsuarioMongo):
    conn = FactoriaMongo.getConexion()
    db = conn["tfg"]
    coll = db["users"]
    nuevo_usuario = dict(user)
    coll.insert_one(nuevo_usuario)
    conn.close()
    return "Usuario creado"


@router.put("/usuarios/{id}")
def put_Usuario(id: str, user: UsuarioMongo):
    conn = FactoriaMongo.getConexion()
    db = conn["tfg"]
    coll = db["users"]
    result = coll.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": dict(user)}
    )
    conn.close()
    return result


@router.delete("/usuarios/{id}")
def delete_Usuario(id):
    conn = FactoriaMongo.getConexion()
    db = conn["tfg"]
    coll = db["users"]
    myquery = {"_id": ObjectId(id)}
    coll.delete_one(myquery)
    conn.close()
    return "Usuario Borrado con éxito"

@router.get("/usuarios/usersWithReviews/{count}")
def get_Users_With_X_Reviews(count):
    conn = FactoriaMongo.getConexion()
    db = conn["tfg"]
    coll = db["users"]
    usuarios = coll.find(
        {"numReviewsEnBD": {"$gte": int(count)}}
    )
    conn.close()
    return usuariosEntity(usuarios)


@router.get("/usuarios/{count}")
def get_Users_With_X_Reviews_Algorythm(count):
    conn = FactoriaMongo.getConexion()
    db = conn["tfg"]
    coll = db["users"]
    usuarios = coll.find(
        {"numReviewsEnBD": {"$gte": int(count)}},
        {"_id": 1}
    )
    conn.close()
    return usuariosAlgoritmoEntity(usuarios)
