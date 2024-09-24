import asyncio
import os
import smtplib
from dotenv import load_dotenv

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from config.log_config import error_logger
from crud.options import options_crud
from models.options.code_model import CodeModel
from services.auth import auth_services

load_dotenv()


async def send_feedback(sender: str, message: str):
    try:
        pass
    except Exception as e:
        error_logger.error(f"Could was not possible to send feedback. Error: {e}")
        raise HTTPException(status_code=400, detail={"Error": f"Could was not possible to send feedback. Error: {e}"})


async def delete_code(db: AsyncSession, code: CodeModel):
    await asyncio.sleep(60)
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
        sender_mail = os.getenv("EMAIL_RECIPIENT")
        sender_password = os.getenv("EMAIL_HOST_PASSWORD")

        mailsender = smtplib.SMTP(os.getenv("EMAIL_HOST"), int(os.getenv("EMAIL_PORT")))

        mailsender.starttls()

        mailsender.login(sender_mail, sender_password)

        mail_subject = 'Код восстановления пароля'
        mail_body_text = "Здравствуйте,\n\nВот ваш код восстановления пароля: " + str(code_obj.code)

        mail_body_html = f"""
        <html>
          <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #fff; border-radius: 10px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); padding: 20px;">

              <h2 style="color: #333; text-align: center;">Код для восстановления пароля</h2>

              <p style="font-size: 16px; color: #555;">
                Здравствуйте,
              </p>

              <p style="font-size: 16px; color: #555;">
                Вы запросили восстановление пароля. Используйте следующий код для восстановления доступа к вашему аккаунту:
              </p>

              <div style="text-align: center; margin: 20px 0;">
                <p style="font-size: 24px; color: #fff; background-color: #007BFF; padding: 10px 20px; border-radius: 5px; display: inline-block;">
                  {code_obj.code}
                </p>
              </div>

              <p style="font-size: 16px; color: #555;">
                Если вы не запрашивали восстановление пароля, просто проигнорируйте это письмо.
              </p>

              <p style="font-size: 16px; color: #555;">
                С уважением,<br>
                Команда поддержки
              </p>

              <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
              <p style="font-size: 12px; color: #888; text-align: center;">
                Это письмо было отправлено автоматически. Пожалуйста, не отвечайте на него.
              </p>
            </div>
          </body>
        </html>
        """
        msg = MIMEMultipart('alternative')
        msg['Subject'] = mail_subject
        msg['From'] = sender_mail
        msg['To'] = email

        msg.attach(MIMEText(mail_body_text, 'plain', 'utf-8'))
        msg.attach(MIMEText(mail_body_html, 'html', 'utf-8'))

        mailsender.sendmail(sender_mail, email, msg.as_string())
        mailsender.quit()
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


async def check_code(db: AsyncSession, email: str, code: int):
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
