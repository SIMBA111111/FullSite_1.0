import os

from smtplib import SMTP
from email.mime.text import MIMEText

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from config.log_config import error_logger
from crud.options import options_crud
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


async def user_is_email(db: AsyncSession, username: str, email: str):
    try:
        await options_crud.user_is_email(db, username, email)
    except Exception as e:
        error_logger.error(f"Could сопоставить юзера и почту. Error: {e}")
        raise HTTPException(status_code=400, detail={"Error": f"Could сопоставить юзера и почту. Error: {e}"})
    return True


async def send_reset_code(db: AsyncSession, username: str, email: str):
    try:
        code_obj = await options_crud.create_code(db, username, email)
    except Exception as e:
        error_logger.error(f"Could создать код. Error: {e}")
        raise HTTPException(status_code=400, detail={"Error": f"Could создать код. Error: {e}"})
    #
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
        error_logger.error(f"Could отправить почту. Error: {e}")
        raise HTTPException(status_code=400, detail={"Error": f"Could отправить почту. Error: {e}"})

    try:
        await options_tasks.task_delete_code(db, code_obj)
    except Exception as e:
        error_logger.error(f"Could запустить таймер и удаление сода. Error: {e}")
        raise HTTPException(status_code=400, detail={"Error": f"Could  запустить таймер и удаление сода. Error: {e}"})


async def check_code(db: AsyncSession, username: str, email: str, code: str):
    try:
        code_exist = await options_crud.check_code_exists(db, username, email, code)
        print(code_exist)
    except Exception as e:
        error_logger.error(f"Could проверить код. Error: {e}")
        raise HTTPException(status_code=400, detail={"Error": f"Could  проверить код. Error: {e}"})
    return code_exist


async def new_password(db: AsyncSession, new_password: str, email: str):
    try:
        new_hashed_password = await auth_services.is_hashed_password(new_password)
        x = await options_crud.change_password(db, new_hashed_password, email)
    except Exception as e:
        error_logger.error(f"Could. Error: {e}")
        raise HTTPException(status_code=400, detail={"Error": f"Could поменять пароль. Error: {e}"})
    # return code_exist