from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    login: str
    password: str
    email: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserGet(BaseModel):
    id: int
    login: str
    email: str
    email_verified: bool
    create_date: str
    subscription_started: str
    subscription_months: int
    discord_linked: bool
    discord_oauth: str

    class Config:
        orm_mode = True


class PlayerCreate(BaseModel):
    uuid: str


class PlayerGet(BaseModel):
    uuid: str

    class Config:
        orm_mode = True


class FondyPayment(BaseModel):
    order_id: str
    merchant_id: int
    amount: int
    currency: str
    order_status: str
    response_status: str
    signature: str
    tran_type: str
    sender_cell_phone: str
    sender_account: str
    masked_card: str
    card_bin: int
    card_type: str
    rrn: str
    approval_code: str
    response_code: int
    response_description: str
    reversal_amount: int
    settlement_amount: int
    settlement_currency: str
    order_time: str
    settlement_date: str
    eci: int
    fee: int
    payment_system: str
    sender_email: str
    payment_id: int
    actual_amount: int
    actual_currency: str
    product_id: str
    merchant_data: str
    verification_status: str
    rectoken: str
    rectoken_lifetime: str
    additional_info: str
