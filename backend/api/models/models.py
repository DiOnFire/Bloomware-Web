from pydantic import BaseModel


class User(BaseModel):
    login: str
    password: str
    subscription_started: str = "none"
    subscription_months: int = -1
    hwids: str = "[]"
    sessions: str = "[]"
    email: str
    email_verified: bool = False
    create_date: str
    discord_linked: bool = False
    discord_oauth: str = "null"
    discord_id: int = -1


class Player(BaseModel):
    uuid: str
