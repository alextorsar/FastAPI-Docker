from bson.objectid import ObjectId
from fastapi import APIRouter, Depends
from app.auth.auth_handler import signJWT
from app.bd import FactoriaMongo, FactoriaSQL
from app.schemas.usuario import usuarioEntity, usuariosEntity, usuariosAlgoritmoEntity, usuariosEntitySQL, \
    convertUserSQLToMongo
from app.models.usuario import UsuarioMongo, UsuarioSQL, UserLoginSchema
from app.utils.utils import findIdArtificialUsuarioSQL
from cryptography.fernet import Fernet
from app.auth.auth_bearer import JWTBearer
import app.utils.db as db

key = db.SALT.encode('utf-8')
cipher_suite = Fernet(key)

usuario = APIRouter(
    tags=["Usuarios"]
)


@usuario.get("/usuarios")
def get_Usuarios():
    conn = FactoriaMongo.getConexion()
    db = conn["tfg"]
    coll = db["users"]
    result = coll.find({})
    usuarios = usuariosEntity(result)
    conn.close()
    return usuarios


@usuario.get("/usuarios/{id}",dependencies=[Depends(JWTBearer())])
def get_Usuario(id):
    conn = FactoriaMongo.getConexion()
    db = conn["tfg"]
    coll = db["users"]
    usuario_bd = usuarioEntity(coll.find_one({"_id": ObjectId(id)}))
    conn.close()
    return dict(usuario_bd)


@usuario.post("/usuarios/signup")
async def create_Usuarios(user: UsuarioSQL):
    connMongo = FactoriaMongo.getConexion()
    db = connMongo["tfg"]
    coll = db["users"]
    userMongo = convertUserSQLToMongo(user)
    nuevo_usuario = dict(userMongo)
    idUsuario = coll.insert_one(nuevo_usuario).inserted_id
    connMongo.close()
    idUsuario = str(idUsuario)
    contraseniaCifrada = cipher_suite.encrypt(user.Contraseña.encode('utf-8'))
    connSQL = FactoriaSQL.getConexion()
    sentencia = "INSERT INTO bd_relacional.usuario VALUES (%s, %s, %s, %s, %s, %s, %s)"
    cursor = connSQL.cursor()
    cursor.execute(sentencia, (idUsuario, user.CorreoElectronico, user.Genero, contraseniaCifrada,
                               user.FechaNac.strftime('%Y-%m-%d'), user.Direccion, user.Nombre))
    connSQL.commit()
    connSQL.close()
    return signJWT(idUsuario)


def check_user_exists(data: UserLoginSchema):
    connSQL = FactoriaSQL.getConexion()
    sentencia = "SELECT * FROM bd_relacional.usuario where bd_relacional.usuario.CorreoElectronico = %s;"
    cursor = connSQL.cursor()
    if cursor.execute(sentencia, data.email) == 1:
        return True
    else:
        return False


def check_login_info(data: UserLoginSchema):
    connSQL = FactoriaSQL.getConexion()
    sentencia = "SELECT Contraseña FROM bd_relacional.usuario where bd_relacional.usuario.CorreoElectronico = %s;"
    cursor = connSQL.cursor()
    cursor.execute(sentencia, data.email)
    result = cursor.fetchone()
    password = str(result['Contraseña'])
    connSQL.close()
    if cipher_suite.decrypt(password) == data.password.encode('utf-8'):
        return True
    else:
        return False


@usuario.post("/user/login")
async def user_login(user: UserLoginSchema):
    if check_user_exists(user) and check_login_info(user):
        connSQL = FactoriaSQL.getConexion()
        sentencia = "SELECT * FROM bd_relacional.usuario where bd_relacional.usuario.CorreoElectronico = %s;"
        cursor = connSQL.cursor()
        cursor.execute(sentencia, user.email)
        result = cursor.fetchone()
        idUsuario = str(result['idUsuario'])
        connSQL.close()
        return {
            "idUsuario": idUsuario,
            "CorreoElectronico": str(result['CorreoElectronico']),
            "Genero": str(result['Genero']),
            "FechaNac": str(result['FechaNac']),
            "Direccion": str(result['Direccion']),
            "Nombre": str(result['Nombre']),
            "accesstoken": signJWT(idUsuario)
        }
    else:
        return {
            "error": "Wrong login details!"
        }


@usuario.put("/usuarios/{id}", dependencies=[Depends(JWTBearer())])
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


@usuario.delete("/usuarios/{id}", dependencies=[Depends(JWTBearer())])
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
