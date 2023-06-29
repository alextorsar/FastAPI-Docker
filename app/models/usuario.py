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
    Name: str
    Email: str
    Gender: str
    Password: str
    Date: str
    Address: str
    Vegano: bool


class UserLoginSchema(BaseModel):
    email: str
    password: str
