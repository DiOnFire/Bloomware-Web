from typing import Optional, Any

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from backend.api.store import SESSION_FACTORY_PLAY
from backend.api.store.models.models import Player


def add_player(session: Session, player: Player) -> None:
    """ Adds user via session and player instance """
    session.add(player)
    session.commit()


def get_player_by_id(user_id: int) -> Player:
    """ Gets user instance from database via id """
    with SESSION_FACTORY_PLAY() as session:
        session: Session
        return session.query(Player).filter_by(id=user_id).all()


def get_player_by_uuid(session: Session, uuid: str) -> Optional[Any]:
    """ Gets user instance from database via UUID """
    try:
        return session.query(Player).filter_by(uuid=uuid).first()
    except NoResultFound:
        return None


def delete_player(user_id: int) -> None:
    """ Gets player from database via ID and deletes him """
    with SESSION_FACTORY_PLAY() as session:
        session: Session
        player = session.query(Player).filter_by(id=user_id).first()
        session.delete(player)
        session.commit()


def delete_player_via_uuid(uuid: str) -> None:
    """ Gets player from database via UUID and deletes him """
    with SESSION_FACTORY_PLAY() as session:
        session: Session
        player = session.query(Player).filter_by(uuid=uuid).first()
        session.delete(player)
        session.commit()


def get_online_players_count() -> int:
    """ Gets count of online players """
    with SESSION_FACTORY_PLAY() as session:
        session: Session
        return session.query(Player).count()
