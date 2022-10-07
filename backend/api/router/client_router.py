from fastapi import APIRouter

from backend.api.store import players
from backend.api.traits import LATEST_VERSION

client_router = APIRouter()


@client_router.get("/api/client/latest")
def get_latest_version():
    return {"latest_version": LATEST_VERSION}


@client_router.get("/api/client/compare")
def compare_version(version: str):
    return {"outdated": float(version) < float(LATEST_VERSION)}


@client_router.get("/api/client/stats")
def get_stats():
    return {"online": players.get_online_players_count()}
