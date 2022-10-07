from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from backend.api.models.schemas import PlayerCreate
from backend.api.store import SESSION_FACTORY_PLAY, players
from backend.api.store.models.models import Player
from backend.api.util import validation_util

play_router = APIRouter()


def get_database():
    database = SESSION_FACTORY_PLAY()
    try:
        yield database
    finally:
        database.close()


@play_router.get("/api/play/playing/{uuid}")
def is_playing(uuid: str, session: Session = Depends(get_database)):
    return {"playing": players.get_player_by_uuid(session, uuid) is not None}


@play_router.post("/api/play/register")
def register_player(player: PlayerCreate, session: Session = Depends(get_database)):
    player_dict: dict = player.dict()
    if not validation_util.is_correct_uuid(player_dict["uuid"]):
        return JSONResponse(status_code=402)
    try:
        players.add_player(session, Player(**player.dict()))
        return JSONResponse(status_code=200)
    except Exception:
        return JSONResponse(status_code=402)


@play_router.post("/api/play/remove")
def remove_player(uuid: str):
    try:
        players.delete_player_via_uuid(uuid)
        return JSONResponse(status_code=200)
    except Exception:
        return JSONResponse(status_code=401)
