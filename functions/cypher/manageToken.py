from warnings import catch_warnings
import jwt
from decouple import config
from datetime import datetime, timedelta

SECRET_KEY = config("SECRET_KEY")
ALGORITHM = config("ALGORITHM")


def generate_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=30)):
    expire = datetime.utcnow() + expires_delta
    token_data = {}
    for key in data:
        token_data[key] = data[key]
    token_data["exp"] = expire
    print(token_data)
    encoded_jwt = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        return {
            "payload": payload,
            "success": True,
        }

    except Exception as e:
        return {
            "exception": e,
            "success": False,
        }
