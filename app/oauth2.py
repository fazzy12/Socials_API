from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = "c280d3acf37fa0f88bbd97d6a69d04369496ce3de5cd041f5bc9e3593b7c22cf"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_be_encoded = data.copy()

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_be_encoded.update({"expire": expire.isoformat()})

    encoded_jwt = jwt.encode(to_be_encoded, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt
