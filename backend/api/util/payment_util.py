import random

from cloudipsp import Api, Checkout
from cloudipsp.helpers import get_signature
from sqlalchemy.orm import Session

from backend.api.store import SESSION_FACTORY_KEY
from backend.api.store.models.models import Key


def generate_order_id():
    return random.randint(1, 99999999999)


def get_payment_link() -> str:
    api = Api(merchant_id=1505186,
              secret_key='zpGZajb5kA07207iOnHAPufQuXSMHMlh')
    checkout = Checkout(api=api)
    data = {
        "currency": "USD",
        "amount": 500,
        "order_id": generate_order_id(),
        "order_desc": "One month of Bloomware subscription.",
        "merchant_id": 1505186,
    }
    sign = get_signature('zpGZajb5kA07207iOnHAPufQuXSMHMlh', data, "1.0")
    data["signature"] = sign
    url = checkout.url(data).get('checkout_url')
    add_to_db(data["order_id"], sign)
    return url


def add_to_db(order_id: int, sign: str):
    with SESSION_FACTORY_KEY() as session:
        session: Session
        key = Key()
        key.key = order_id
        key.sign = sign
        session.add(key)
        session.commit()
