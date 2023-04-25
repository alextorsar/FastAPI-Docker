from app.models.restaurante import RestauranteSQL, Photo, PlusCode
from app.models.restaurante import Geometry
from app.models.restaurante import Coordenada
from typing import Optional


def restauranteEntitySQL(item) -> dict:
    if item["price_level"] is not None:
        price_level = item["price_level"]
    else:
        price_level = None
    return {
        "oid": item["idrestaurante"],
        "formatted_address": item["localizacion"],
        "lat": item["latitud"],
        "lng": item["longitud"],
        "name": item["nombre"],
        "photo_url": item["foto_URL"],
        "place_id": item["place_id"],
        "price_level": price_level,
        "rating": item["rating"],
        "types": None,
        "user_ratings_total": item["num_reviews"]
    }

def restaurantesEntitySQL(restaurantes) -> dict:
    return [restauranteEntitySQL(item) for item in restaurantes]


def restauranteEntityMongo(item) -> dict:
    if ("price_level" in item):
        price_level = item["price_level"]
    else:
        price_level = None
    return {
        "oid": str(item["_id"]),
        "business_status": item["business_status"],
        "formatted_address": item["formatted_address"],
        "lat": item["geometry"]["location"]["lng"],
        "lng": item["geometry"]["location"]["lat"],
        "name": item["name"],
        "photo_url": item["photo_url"],
        "place_id": item["place_id"],
        "price_level": price_level,
        "rating": item["rating"],
        "types": item["types"],
        "user_ratings_total": item["user_ratings_total"]
    }


def restaurantesEntityMongo(restaurantes) -> dict:
    return [restauranteEntityMongo(item) for item in restaurantes]


def restauranteAlgoritmoEntity(item, idArtificial) -> dict:
    if "_id" in item.keys():
        id = str(item["_id"])
    else:
        id = str(item["restaurantOid"])

    return {
        "oid": id,
        "id": idArtificial
    }


def restaurantesAlgoritmoEntity(restaurantes) -> list:
    idArtificial = 1
    result = list()
    for restaurante in restaurantes:
        result.append(restauranteAlgoritmoEntity(restaurante, idArtificial))
        idArtificial = idArtificial + 1
    return result


def restauranteEntityId(item) -> dict:
    return {
        "oid": str(item["_id"])
    }


def restaurantesEntityId(restaurantes) -> list:
    return [restauranteEntityId(item) for item in restaurantes]

def transformarEsquemaRelacionalAMongo(restaurante: RestauranteSQL)->dict:
    return {
        "business_status": Optional[str],
        "formatted_address": restaurante.localizacion,
        "geometry": Geometry(),
        "icon": str,
        "icon_background_color": Optional[str],
        "icon_mask_base_uri": Optional[str],
        "name": restaurante.nombre,
        "photos": Optional[list[Photo]],
        "place_id": str,
        "plus_code": Optional[PlusCode],
        "price_level": Optional[restaurante.price_level],
        "rating": restaurante.rating,
        "reference": Optional[str],
        "types": Optional[list[str]],
        "user_ratings_total": int,
        "photo_url": restaurante.foto_URL,

        #"formatted_address": RestauranteSQL["localizacion"],
        #"geometry": Geometry(),
        #icon: Optional[str],
        #icon_background_color: Optional[str],
        #icon_mask_base_uri: Optional[str],
        #name: str,
        #photos: Optional[list[Photo]],
        #place_id: str,
        #plus_code: Optional[PlusCode],
        #price_level: Optional[int],
        #rating: float,
        #reference: Optional[str],
        #types: Optional[list[str]],
        #user_ratings_total: int,
        #photo_url: str,
    }