import datetime
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from backend.api import traits
from backend.api.exception.SameEmailExistError import SameEmailExistError
from backend.api.exception.SameNicknameExistError import SameNicknameExistError
from backend.api.models.models import User
from jose import jwt
from backend.api.store import users
from backend.api.traits import SECRET_KEY, ALGORITHM


PWD_CONTEXT = CryptContext(schemes=["bcrypt"])


def register(session: Session, user: User):
    user.password = PWD_CONTEXT.hash(user.password)
    user.email_verified = False
    user.create_date = datetime.datetime.now()
    user.two_factor_auth = False
    user.subscription = False
    user.discord_oauth = "null"
    user.discord_linked = False
    user.subscription_months = 0
    user.subscription_started = "null"
    try:
        users.add_user(session, user)
    except IntegrityError as exception:
        print(str(exception))
        if str(exception).find("users.nickname") != -1:
            raise SameNicknameExistError()
        if str(exception).find("users.email") != -1:
            raise SameEmailExistError()


def verify_pass(password: str, hash_password: str):
    return PWD_CONTEXT.verify(password, hash_password)


def generate_token(user: User) -> str:
    """ Generates access token """
    data = {
        "exp": datetime.datetime.now() + datetime.timedelta(minutes=traits.ACCESS_TOKEN_EXPIRE_MINUTES),
        "sub": user.login
    }
    return jwt.encode(data, SECRET_KEY, ALGORITHM)[::-1]


def generate_token_nick(nickname: str) -> str:
    data = {
        "exp": datetime.datetime.now() + datetime.timedelta(minutes=traits.ACCESS_TOKEN_EXPIRE_MINUTES),
        "sub": nickname
    }
    return jwt.encode(data, SECRET_KEY, ALGORITHM)[::-1]


def auth(session: Session, login: str, password: str):
    user = users.get_user_by_username(session, login)
    if user is None:
        raise ValueError("No user!")
    valid = verify_pass(password, user.password)
    if not valid:
        raise ValueError("Incorrect password!")
    return generate_token(user)


