import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from backend.api.database.auth import current_user
from backend.api.models.models import User
from backend.api.models.schemas import FondyPayment
from backend.api.store import SESSION_FACTORY_CLIENT, users, keys, SESSION_FACTORY_KEY
from backend.api.store.models.models import Key
from backend.api.store.users import apply_subscription
from backend.api.util import key_util

key_router = APIRouter()


@key_router.post("/api/fondy/callback")
def generate_key(metadata: FondyPayment):
    with SESSION_FACTORY_KEY() as session:
        session: Session
        try:
            key: Key = session.query(Key).filter_by(key=metadata.order_id).first()
            if metadata.signature == key.sign:
                user: User = current_user(key.used_by)
                if user and metadata.order_status == "approved":
                    apply_subscription(user)
        except NoResultFound:
            pass
