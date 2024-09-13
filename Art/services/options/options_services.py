import asyncio
import os

from smtplib import SMTP
from email.mime.text import MIMEText

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from config.log_config import error_logger
from crud.options import options_crud
from models.options.code_model import CodeModel
from services.auth import auth_services


async def send_feedback(sender: str, message: str):
    try:
        EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
        EMAIL_PORT = os.getenv("EMAIL_PORT", "587")
        EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "qqhs ptld aivs lwrl")
        EMAIL_RECIPIENT = os.getenv("EMAIL_RECIPIENT", "naaro2930@gmail.com")

        server = SMTP(host=EMAIL_HOST, port=EMAIL_PORT)
        server.connect(host=EMAIL_HOST, port=EMAIL_PORT)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(user=sender, password=EMAIL_HOST_PASSWORD)

        msg = MIMEText(message)
        msg['subject'] = 'Обратная связь моего сайта'
        msg['From'] = sender
        msg['To'] = EMAIL_RECIPIENT

        server.sendmail(sender, EMAIL_RECIPIENT, msg.as_string())

        server.quit()
    except Exception as e:
        error_logger.error(f"Could was not possible to send feedback. Error: {e}")
        raise HTTPException(status_code=400, detail={"Error": f"Could was not possible to send feedback. Error: {e}"})


async def delete_code(db: AsyncSession, code: CodeModel):
    await asyncio.sleep(60 * 5)
    try:
        await options_crud.delete_code(db, code)
    except Exception as e:
        error_logger.error(f"Couldn't delete the code. Error: {e}")
        raise HTTPException(status_code=400, detail={"Error": f"Couldn't delete the code. Error: {e}"})


async def user_exist(db: AsyncSession, email: str):
    try:
        await options_crud.user_exist(db, email)
    except Exception as e:
        error_logger.error(f"There is no user with such an email. Error: {e}")
        raise HTTPException(status_code=400, detail={"Error": f"ЕThere is no user with such an email. Error: {e}"})
    return True


async def send_reset_code(db: AsyncSession, email: str):
    try:
        code_obj = await options_crud.create_code(db, email)
    except Exception as e:
        error_logger.error(f"Couldn't create the code. Error: {e}")
        raise HTTPException(status_code=400, detail={"Error": f"Couldn't create the code. Error: {e}"})

    try:
        EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
        EMAIL_PORT = os.getenv("EMAIL_PORT", "587")
        EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "qqhs ptld aivs lwrl")
        EMAIL_RECIPIENT = os.getenv("EMAIL_RECIPIENT", "naaro2930@gmail.com")

        server = SMTP(host=EMAIL_HOST, port=EMAIL_PORT)
        server.connect(host=EMAIL_HOST, port=EMAIL_PORT)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(user=email, password=EMAIL_HOST_PASSWORD)

        mail_html = f"<h1>Код для восстановления паролья:</h1> <p style='background: red'>{code_obj.code}</p>"

        msg = MIMEText(mail_html, "html")
        msg['subject'] = 'Код восстановления пароля'
        msg['From'] = email
        msg['To'] = EMAIL_RECIPIENT

        server.sendmail(email, EMAIL_RECIPIENT, msg.as_string())
    except Exception as e:
        error_logger.error(f"Couldn't send code to the email. Error: {e}")
        raise HTTPException(status_code=400, detail={"Error": f"Couldn't send code to the email. Error: {e}"})

    try:
        await delete_code(db, code_obj)
    except Exception as e:
        error_logger.error(f"Couldn't start the timer and delete the code. Error: {e}")
        raise HTTPException(status_code=400,
                            detail={"Error": f"Couldn't start the timer and delete the code. Error: {e}"}
                            )


async def check_code(db: AsyncSession, email: str, code: str):
    try:
        code_exist = await options_crud.check_code_exists(db, email, code)
    except Exception as e:
        error_logger.error(f"Couldn't check password. Error: {e}")
        raise HTTPException(status_code=400, detail={"Error": f"Couldn't check password. Error: {e}"})
    return code_exist


async def new_password(db: AsyncSession, new_password: str, email: str):
    try:
        new_hashed_password = await auth_services.is_hashed_password(new_password)
        await options_crud.change_password(db, new_hashed_password, email)
    except Exception as e:
        error_logger.error(f"Couldn't change your password. Error: {e}")
        raise HTTPException(status_code=400, detail={"Error": f"Couldn't change password. Error: {e}"})
    return True
