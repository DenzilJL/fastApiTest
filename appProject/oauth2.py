from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schema
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from .config import OAUTH_ACCESS_TOKEN_EXPIRE_MINUTES, OAUTH_ALGORITHM, OAUTH_SECRET_KEY
# secret key
# algorithm
# expire time
SECRET_KEY = OAUTH_SECRET_KEY
ALGORITHM = OAUTH_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = OAUTH_ACCESS_TOKEN_EXPIRE_MINUTES

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return token


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)

        id: str = payload.get("user_id")
        if id is None:
            return credentials_exception
        token_data = schema.TokenData(id=id)
        return token_data
    except JWTError:
        raise credentials_exception


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"crendials mismatched", headers={"WWW-Authenticate": "Bearer"})
    return verify_access_token(token, credentials_exception)
