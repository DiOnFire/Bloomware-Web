import base64
from hashlib import md5

from jose import jwt, JWTError
from caesarcipher import CaesarCipher

from backend.api.traits import SECRET_KEY_KEY, ALGORITHM, INTERKASSA_SECRET

TARGETS = [
    "BLOOMWARE_LICENCE",
    "CLOUD_SUBSCRIPTION"
]


def generate_key(ik_co_id: str, ik_pm_no: str, ik_desc: str, ik_cur: str, ik_pw_via: str, ik_am: str, ik_act: str,
                 ik_inv_id: str, ik_sign: str, ik_inv_prc: str, ik_inv_st: str) -> str:
    """
    Generates access key
    - Encode key
    - Reverse encoded key
    - Encrypt via caesar
    """
    data = {
        "ik_co_id": ik_co_id,
        "ik_pm_no": ik_pm_no,
        "ik_desc": ik_desc,
        "ik_cur": ik_cur,
        "ik_pw_via": ik_pw_via,
        "ik_am": ik_am,
        "ik_act": ik_act,
        "ik_inv_id": ik_inv_id,
        "ik_sign": ik_sign,
        "ik_inv_prc": ik_inv_prc,
        "ik_inv_st": ik_inv_st
    }
    return CaesarCipher(jwt.encode(data, SECRET_KEY_KEY, ALGORITHM)[::-1], offset=15).encoded


def validate_key(token: str) -> bool:
    try:
        token = CaesarCipher(token[::-1], offset=15).decoded
        jwt.decode(token, SECRET_KEY_KEY, ALGORITHM)
    except JWTError:
        return False
    return True


def generate_ik_sign(metadata: dict) -> str:
    data = []
    for key in sorted(metadata.keys()):
        if key.startswith("ik_") and key != "ik_sign":
            data.append(metadata[key])
    data.append(INTERKASSA_SECRET)
    return base64.b64encode(md5(":".join(data).encode()).digest()).decode()


def validate_ik(key: str) -> bool:
    token = CaesarCipher(key[::-1], offset=15).decoded
    metadata: dict = jwt.decode(token, SECRET_KEY_KEY, ALGORITHM)
    sign = generate_ik_sign(metadata)
    return sign == metadata["ik_sign"]
