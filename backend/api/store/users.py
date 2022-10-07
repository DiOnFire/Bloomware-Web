import datetime
from typing import Optional, Any

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from backend.api.store import SESSION_FACTORY_CLIENT
from backend.api.store.models.models import User


def add_user(session: Session, user: User):
    """ Adds user via session and user instance """
    session.add(user)
    session.commit()


def get_user_by_id(user_id: int) -> User:
    """ Gets user instance from database via id """
    with SESSION_FACTORY_CLIENT() as session:
        session: Session
        return session.query(User).filter_by(id=user_id).all()


def get_user_by_username(session: Session, username: str) -> Optional[Any]:
    """ Gets user instance from database via nickname """
    try:
        return session.query(User).filter_by(login=username).first()
    except NoResultFound:
        return None


def get_user_by_email(session: Session, email: str) -> Optional[Any]:
    """ Gets user instance from database via email """
    try:
        return session.query(User).filter_by(email=email).first()
    except NoResultFound:
        return None


def update_user(user_id: int, new_instance: User) -> None:
    """ Updates user via id by other instance """
    with SESSION_FACTORY_CLIENT() as session:
        session: Session
        user = session.query(User).filter_by(id=user_id).first()
        user.login = new_instance.login
        user.password = new_instance.password
        user.email = new_instance.email
        user.subscription_started = new_instance.subscription_started
        user.subscription_months = new_instance.subscription_months
        user.discord_oauth = new_instance.discord_oauth
        user.discord_linked = new_instance.discord_linked
        user.email_verified = new_instance.email_verified
        user.discord_id = new_instance.discord_id
        session.commit()


def delete_user(user_id: int) -> None:
    """ Deletes user via id """
    with SESSION_FACTORY_CLIENT() as session:
        session: Session
        user = session.query(User).filter_by(id=user_id).first()
        session.delete(user)
        session.commit()


def get_all_users() -> Any:
    """ Gets all users from database """
    with SESSION_FACTORY_CLIENT() as session:
        session: Session
        return session.query(User).all()


def update_subscription(user: User, value: bool) -> None:
    """ Updates user subscription """
    with SESSION_FACTORY_CLIENT() as session:
        session: Session
        user.subscription = value
        session.commit()


def link_discord(user: User, discord_oauth: str) -> None:
    """ Links Discord and a user account via Discord token """
    with SESSION_FACTORY_CLIENT() as session:
        session: Session
        user.discord_linked = True
        user.discord_oauth = discord_oauth
        session.commit()


def unlink_discord(user: User) -> None:
    """ Unlinks Discord from a user account """
    with SESSION_FACTORY_CLIENT() as session:
        session: Session
        user.discord_linked = False
        user.discord_oauth = None
        session.commit()


def get_user_by_discord(discord_id: int) -> Optional[Any]:
    with SESSION_FACTORY_CLIENT() as session:
        session: Session
        try:
            return session.query(User).filter_by(discord_id=discord_id).first()
        except NoResultFound:
            return None


def apply_subscription(user: User):
    with SESSION_FACTORY_CLIENT() as session:
        session: Session
        if user.subscription_started != "null":
            sub_started = datetime.datetime.strptime(user.subscription_started, "%Y-%m-%d %H:%M:%S")
            delta = datetime.datetime.now() - sub_started
            if delta.days / 30 >= user.subscription_months:
                user.subscription_started = datetime.datetime.now()
                user.subscription_months = 1
            else:
                user.subscription_months += 1
        else:
            user.subscription_started = datetime.datetime.now()
            user.subscription_months = 1
        session.commit()
