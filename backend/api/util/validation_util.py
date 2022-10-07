import json
import re
from typing import Optional, Match
from uuid import UUID

import requests

from backend.api.traits import AUTH_KEY_DISCORD

EMAIL_REGEX = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"


def is_correct_email(email: str) -> Optional[Match[str]]:
    return re.search(EMAIL_REGEX, email)


def is_correct_uuid(uuid: str) -> bool:
    try:
        uuid = UUID(uuid, version=4)
    except ValueError:
        return False
    else:
        return True


def is_correct_user_metadata(username: str, password: str, email: str = "test@gmail.com") -> bool:
    return username.find(" ") == -1 and len(username) >= 3 and len(password) >= 8 and is_correct_email(email)


def verify_key():
    pass


def validate_discord_token(token: str) -> int:
    response = requests.get("https://discord.com/api/users/@me", headers={"Authorization": f"Bearer {token}"})
    json_: dict = json.loads(response.text)
    if response.text.find("username") == -1:
        return -1
    return json_["id"]


def validate_auth_key_discord(target: str) -> bool:
    return target == AUTH_KEY_DISCORD
