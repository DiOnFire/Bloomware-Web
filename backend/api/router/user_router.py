from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import HTMLResponse

from backend.api.database.auth import current_user, verify_token
from backend.api.exception.SameEmailExistError import SameEmailExistError
from backend.api.exception.SameNicknameExistError import SameNicknameExistError
from backend.api.models.schemas import UserGet, UserCreate, UserLogin
from backend.api.store import SESSION_FACTORY_CLIENT, users
from backend.api.store.models.models import User
from backend.api.util import auth_util, email_util, validation_util

user_router = APIRouter()


def get_database():
    """ Gets database session factory """
    database = SESSION_FACTORY_CLIENT()
    try:
        yield database
    finally:
        database.close()


@user_router.get("/api/status")
def check_status():
    return {"status": "working"}


@user_router.get("/api/users/verification", response_class=HTMLResponse)
def verify_email(request: Request, token: str):
    user = verify_token(token)

    if user and not user.email_verified:
        new_instance = user
        new_instance.email_verified = True
        users.update_user(user.id, user)


@user_router.post("/api/users/auth")
def auth(user: UserLogin, session: Session = Depends(get_database)):
    if validation_util.is_correct_user_metadata(user.username, user.password):
        try:
            token = auth_util.auth(session, user.username, user.password)
        except ValueError:
            return {"error": "invalid credentials"}
        else:
            return {"access_token": token, "token_type": "bearer"}
    else:
        return {"error": "invalid credentials"}


# @user_router.get("/api/users/id/{user_id}")
# def get_user_by_id(user_id: int, user: User = Depends(current_user)):
#     """ Gets user by id via API request """
#     user = users.get_user_by_id(user_id)
#     return user


@user_router.post("/api/users/create")
async def create_user(user: UserCreate, session: Session = Depends(get_database)):
    """ Creates user via API request """
    user_dict: dict = user.dict()
    if validation_util.is_correct_user_metadata(user.login, user.password, user.email):
        try:
            auth_util.register(session, User(**user_dict))
            # await email_util.send_reg_email(User(**user_dict))
            return {"message": "a new user was successfully registered"}
        except SameNicknameExistError:
            return {"error": "a user with this nickname already exist"}
        except SameEmailExistError:
            return {"error": "a user with this email already exist"}
    else:
        return {"error": "invalid credentials (incorrect email or password too short)"}


# @user_router.post("/api/users/{nickname}", response_model=UserGet)
# def get_user_by_username(nickname: str, session: Session = Depends(get_database)):
#     """ Gets user by username via API request """
#     return users.get_user_by_username(session, nickname)


# @user_router.put("/api/users/subscription/{nickname}")
# def update_subscription(nickname: str, admin: UserGet, value: bool, session: Session = Depends(get_database)):
#     """ Updates subscription status for user via request """
#     user: User = users.get_user_by_username(session, nickname)
#     users.update_subscription(user, value)


@user_router.get("/api/users/me")
def get_me(user: User = Depends(current_user)):
    """ Gets user via token """
    if user is None:
        return {"detail": "Not authenticated"}
    return {
        "id": user.id,
        "login": user.login,
        "email": user.email,
        "email_verified": user.email_verified,
        "subscription_started": user.subscription_started,
        "subscription_months": user.subscription_months,
        "discord_linked": user.discord_linked,
        "discord_id": user.discord_id,
        "discord_oauth": user.discord_oauth,
        "create_date": user.create_date,
    }


@user_router.get("/api/users/discord")
def get_user_by_discord_id(discord_id: int, auth_key: str):
    if validation_util.validate_auth_key_discord(auth_key):
        user: User = users.get_user_by_discord(discord_id)
        if user:
            return {
                "id": user.id,
                "login": user.login,
                "email": user.email,
                "email_verified": user.email_verified,
                "subscription_started": user.subscription_started,
                "subscription_months": user.subscription_months,
                "discord_linked": user.discord_linked,
                "discord_id": user.discord_id,
                "discord_oauth": user.discord_oauth,
                "create_date": user.create_date,
            }
        else:
            return {"error": "not found"}
    else:
        return {"error": "not found"}


@user_router.get("/api/users/me/discord")
def get_discord(user: User = Depends(current_user)):
    return {"linked": user.discord_linked, "token": user.discord_oauth}


@user_router.post("/api/users/me/discord/link")
def link_discord(discord_oauth: str, user: User = Depends(current_user)):
    metadata = validation_util.validate_discord_token(discord_oauth)
    if metadata != -1:
        new_instance = user
        new_instance.discord_linked = True
        new_instance.discord_oauth = discord_oauth
        new_instance.discord_id = int(metadata)
        users.update_user(user.id, new_instance)
    else:
        return {"error": "invalid token"}


@user_router.post("/api/users/me/discord/unlink")
def unlink_discord(user: User = Depends(current_user)):
    if user.discord_linked:
        new_instance = user
        new_instance.discord_linked = False
        new_instance.discord_oauth = "none"
        new_instance.discord_id = -1
        users.update_user(user.id, new_instance)
    else:
        return {"error": "discord account not linked"}


@user_router.get("/api/users/me/mail_link")
def send_mail(user: User = Depends(current_user)):
    if not user.email_verified:
        email_util.send_reg_email(user)
    else:
        return {"error": "this user has already verified his email"}


@user_router.post("/api/users/me/password_reset", response_class=HTMLResponse)
def reset_password(token: str, password: str):
    user = verify_token(token)

    if user and len(password) >= 8:
        new_instance: User = user
        new_instance.password = password
        users.update_user(user.id, user)


@user_router.post("/api/users/me/email_change", response_class=HTMLResponse)
def change_email(token: str, email: str):
    user = verify_token(token)
    if user and validation_util.is_correct_email(email):
        new_instance: User = user
        new_instance.email = email
        new_instance.email_verified = False
        users.update_user(user.id, new_instance)
