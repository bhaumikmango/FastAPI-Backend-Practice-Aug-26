from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = '1034f60f88f93c07fef0cd60d091ef0bea346a6830113e65c5a34193c41d9d21'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data : dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp' : expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)

    return encoded_jwt