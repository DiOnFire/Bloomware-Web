import smtplib

from backend.api.models.models import User
from backend.api.store import users
from backend.api.util.auth_util import generate_token


async def send_reg_email(instance: User):
    token = generate_token(instance)

    server = smtplib.SMTP_SSL(host="smtp.yandex.com", port=465)
    server.ehlo()
    server.login("kys", "kys")
    message = f"Verify your account via this link: http://127.0.0.1:8000/api/users/verification?token={token}"
    server.sendmail("kys", instance.email, message)
    server.quit()


async def send_reset_password_email(email: str):
    user: User = users.get_user_by_email(email)

    if user is not None:
        token = generate_token(user.login)
        server = smtplib.SMTP_SSL(host="smtp.yandex.com", port=465)
        server.ehlo()
        server.login("kys", "kys")
        message = f"Reset your password via this link: http://127.0.0.1:8000/api/users/password?token={token}"
        server.sendmail("kys", email, message)
        server.quit()
