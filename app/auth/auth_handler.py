import time
from typing import Dict

import jwt
from decouple import config

JWT_SECRET = "ebaa110b59c15cca6473385640703dcc5f2d2afc99a6aa9e"
JWT_ALGORITHM = "HS256"



def signJWT(user_id: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token
    except:
        return {}
