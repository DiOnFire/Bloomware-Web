from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from starlette.datastructures import Headers

from backend.api.router.client_router import client_router
from backend.api.router.key_router import key_router
from backend.api.router.pages_router import pages_router
from backend.api.router.play_router import play_router
from backend.api.router.user_router import user_router

app = FastAPI()

origins = ["http://185.154.13.102", "http://127.0.0.1:8000", "http://localhost/"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class NoCacheStaticFiles(StaticFiles):
    def is_not_modified(self, response_headers: Headers, request_headers: Headers) -> bool:
        return False


app.mount("/static", NoCacheStaticFiles(directory="static"), name="static")

app.include_router(user_router)
app.include_router(client_router)
app.include_router(play_router)
app.include_router(pages_router)
app.include_router(key_router)
