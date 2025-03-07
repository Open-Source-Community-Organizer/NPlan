from os import environ  # pylint: disable=E0611

from pydantic import EmailStr

from app.utils.email_handler import send_new_password_mail
from app.utils.worker import celery_app

FRONTEND_URL = environ["FRONTEND_URL"]


@celery_app.task
def send_new_password_email_task(email: EmailStr, username: str, password: str):
    try:
        send_new_password_mail(
            sender_name="devpengs",
            username=username,
            from_email="devpengs@gmail.com",
            to_email=email,
            password=password,
        )
        return {"success": f"new password email sent to {username}"}

    except Exception as e:
        print(str(e))