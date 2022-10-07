from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base

BaseUser = declarative_base()
BasePlayer = declarative_base()
BaseKey = declarative_base()


class User(BaseUser):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    login = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    subscription_started = Column(String)
    subscription_months = Column(Integer)
    hwids = Column(String)
    sessions = Column(String)
    email = Column(String, unique=True)
    email_verified = Column(Boolean)
    create_date = Column(String)
    discord_linked = Column(Boolean)
    discord_oauth = Column(String, nullable=True)
    discord_id = Column(Integer)


class Player(BasePlayer):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True)
    uuid = Column(String, unique=True)


class Key(BaseKey):
    __tablename__ = "keys"
    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True, nullable=False)
    used_by = Column(String)
    sign = Column(String, nullable=False)


def init_main(engine):
    BaseUser.metadata.create_all(engine)


def init_players(engine):
    BasePlayer.metadata.create_all(engine)


def init_keys(engine):
    BaseKey.metadata.create_all(engine)
