from fastapi import APIRouter, Body, status, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from config.log_config import info_logger
from dependencies import get_db
from services.options import options_services

router = APIRouter()


@router.post("/feedback")
async def feedback(email: str = Body(),
                   message: str = Body(),
                   ):
    info_logger.info(f" - START feedback")

    await options_services.send_feedback(email, message)

    response = JSONResponse(status_code=status.HTTP_200_OK,
                            content={"Success": "The feedback has been sent successfully"}
                            )
    info_logger.info(f" - SUCCESS feedback")
    return response


@router.post("/reset-password")
async def reset_password(username: str = Body(),
                         email: str = Body(),
                         db: AsyncSession = Depends(get_db)):
    # await options_services.send_reset_code(db, username, email)
    if await options_services.user_is_email(db, username, email):
        await options_services.send_reset_code(db, username, email)


@router.post("/check-code")
async def reset_password(username: str = Body(),
                         email: str = Body(),
                         code: str = Body(),
                         db: AsyncSession = Depends(get_db)):
    print(username)
    print(email)
    print(code)
    x = await options_services.check_code(db, email, username, code)
    return x


@router.post("/new-password")
async def reset_password(new_password: str = Body(),
                         email: str = Body(),
                         db: AsyncSession = Depends(get_db)):
    x = await options_services.new_password(db, new_password, email)
    return x