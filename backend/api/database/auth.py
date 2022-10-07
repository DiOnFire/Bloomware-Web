from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from backend.api import traits
from backend.api.store import SESSION_FACTORY_CLIENT, users


def get_database():
    """ Gets database session factory """
    database = SESSION_FACTORY_CLIENT()
    try:
        yield database
    finally:
        database.close()


auth_scheme = OAuth2PasswordBearer(tokenUrl="token")


def current_user(token: str = Depends(auth_scheme), session: Session = Depends(get_database)):
    try:
        token = token[::-1]
        data = jwt.decode(token, traits.SECRET_KEY, traits.ALGORITHM)
    except JWTError:
        return None
    if data.get("sub") is None:
        return None
    user = users.get_user_by_username(session, data["sub"])
    return user


def verify_token(token: str, session: Session = Depends(get_database)):
    payload = jwt.decode(token, traits.SECRET_KEY, traits.ALGORITHM)[::-1]
    return users.get_user_by_username(SESSION_FACTORY_CLIENT(), payload["sub"])
