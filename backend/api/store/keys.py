import datetime

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from backend.api.store import SESSION_FACTORY_KEY
from backend.api.store.models.models import Key


def add_key(key_raw: str, ik_co_id: str, ik_pm_no: str, ik_desc: str, ik_cur: str, ik_pw_via: str, ik_am: str,
            ik_act: str,
            ik_inv_id: str, ik_sign: str, ik_inv_prc: str, ik_inv_st: str) -> None:
    with SESSION_FACTORY_KEY() as session:
        session: Session
        key = Key()
        key.key = key_raw
        key.activated = False
        key.created_in = datetime.datetime.now()
        key.used_by = -1
        key.activated_in = "null"
        key.ik_co_id = ik_co_id
        key.ik_pm_no = ik_pm_no
        key.ik_desc = ik_desc
        key.ik_cur = ik_cur
        key.ik_pw_via = ik_pw_via
        key.ik_am = ik_am
        key.ik_act = ik_act
        key.ik_inv_id = ik_inv_id
        key.ik_sign = ik_sign
        key.ik_inv_prc = ik_inv_prc
        key.ik_inv_st = ik_inv_st
        session.add(key)
        session.commit()


def get_key(key: str):
    with SESSION_FACTORY_KEY() as session:
        session: Session
        try:
            return session.query(Key).filter_by(key=key).first()
        except NoResultFound:
            return None


def activate_key(key: Key, new_instance: Key):
    with SESSION_FACTORY_KEY() as session:
        session: Session
        key = session.query(Key).filter_by(key=key).first()
        key.activated = new_instance.activated
        key.activated_in = new_instance.activated_in
        key.used_by = new_instance.used_by
        session.commit()
