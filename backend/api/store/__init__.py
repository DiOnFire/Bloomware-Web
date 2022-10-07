import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.api.store.models import models

PATH_CLIENT = os.environ.get("DATABASE_CLIENT", "sqlite:///bloomware.db")
PATH_PLAY = os.environ.get("DATABASE_PLAY", "sqlite:///players.db")
PATH_KEYS = os.environ.get("DATABASE_KEY", "sqlite:///keys.db")
ENGINE_CLIENT = create_engine(PATH_CLIENT, echo=True)
ENGINE_PLAY = create_engine(PATH_PLAY, echo=True)
ENGINE_KEY = create_engine(PATH_KEYS, echo=True)
SESSION_FACTORY_CLIENT = sessionmaker(ENGINE_CLIENT)
SESSION_FACTORY_PLAY = sessionmaker(ENGINE_PLAY)
SESSION_FACTORY_KEY = sessionmaker(ENGINE_KEY)
try:
    models.init_main(ENGINE_CLIENT)
    models.init_players(ENGINE_PLAY)
    models.init_keys(ENGINE_KEY)
except Exception:
    print("ALREADY INITIALIZED! STARTING...")

