from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import HTMLResponse
from backend.api.util.payment_util import get_payment_link
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="pages")

pages_router = APIRouter()


@pages_router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@pages_router.get("/account")
async def account(request: Request):
    return templates.TemplateResponse("account.html", {"request": request})


@pages_router.get("/account/change_email")
async def account(request: Request):
    return templates.TemplateResponse("change_email.html", {"request": request})


@pages_router.get("/account/change_password")
async def account(request: Request):
    return templates.TemplateResponse("change_password.html", {"request": request})


@pages_router.get("/dashboard")
async def account(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


@pages_router.get("/account/discord_link")
async def account(request: Request):
    return templates.TemplateResponse("discord_link.html", {"request": request})


@pages_router.get("/downloads")
async def account(request: Request):
    return templates.TemplateResponse("downloads.html", {"request": request})


@pages_router.get("/account/email_verify")
async def account(request: Request):
    return templates.TemplateResponse("email_verify.html", {"request": request})


@pages_router.get("/libitida")
async def account(request: Request):
    return templates.TemplateResponse("libitida.html", {"request": request})


@pages_router.get("/login")
async def account(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@pages_router.get("/purchase")
async def account(request: Request):
    return templates.TemplateResponse("purchase.html", {"request": request, "fondy_link": get_payment_link()})


@pages_router.get("/register")
async def account(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@pages_router.get("/account/activate")
async def account(request: Request):
    return templates.TemplateResponse("activate.html", {"request": request})


@pages_router.get("/account/register_verify")
async def account(request: Request):
    return templates.TemplateResponse("register_verify.html", {"request": request})


@pages_router.get("/support")
async def account(request: Request):
    return templates.TemplateResponse("support.html", {"request": request})


@pages_router.get("/terms")
async def account(request: Request):
    return templates.TemplateResponse("terms.html", {"request": request})
