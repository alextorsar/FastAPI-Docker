from pydantic import BaseModel
from typing import Optional

class PlusCode(BaseModel):
    compound_code: str
    global_code: str


class Coordenada(BaseModel):
    lat: float
    lng: float


class Geometry(BaseModel):
    location: Coordenada


class Photo(BaseModel):
    height: int
    width: int
    photo_reference: str
    html_attributions: list[str]


class RestauranteMongo(BaseModel):
    business_status: Optional[str]
    formatted_address: str
    geometry: Geometry
    icon: Optional[str]
    icon_background_color: Optional[str]
    icon_mask_base_uri: Optional[str]
    name: str
    photos: Optional[list[Photo]]
    place_id: str
    plus_code: Optional[PlusCode]
    price_level: Optional[int]
    rating: float
    reference: Optional[str]
    types: Optional[list[str]]
    user_ratings_total: int
    photo_url: str

class RestauranteSQL(BaseModel):
    idrestaurante: Optional[str]
    localizacion: str
    nombre: str
    descripcion: str
    latitud: float
    longitud: float
    foto_URL: str
    place_id: str
    price_level: Optional[int]
    rating: float
    num_reviews: int
