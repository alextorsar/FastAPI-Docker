from enum import Enum
from datetime import date

from pydantic import BaseModel

class Gender(str,Enum):
    Hombre = "Hombre"
    Mujer = "Mujer"
    Otro = "Otro"


class UsuarioMongo(BaseModel):
    name: str
    reviewerId: str
    reviewerUrl: str
    reviewerNumberOfReviews: int
    isLocalGuide: bool
    numReviewsEnBD: int

class UsuarioSQL(BaseModel):
    Nombre: str
    CorreoElectronico: str
    Genero: Gender
    Contraseña: str
    FechaNac: date
    Direccion: str

class UserLoginSchema(BaseModel):
    email: str
    password: str
