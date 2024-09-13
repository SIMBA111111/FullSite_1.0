from fastapi import APIRouter, Body, status, Depends, HTTPException
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
async def reset_password(email: str = Body(),
                         db: AsyncSession = Depends(get_db)):
    info_logger.info(f" - START reset password")

    if await options_services.user_exist(db, email):
        await options_services.send_reset_code(db, email)
    else:
        raise HTTPException(status_code=400, detail={"Error": f"There is no user with such an email"})
    response = JSONResponse(status_code=status.HTTP_200_OK,
                            content={"Success": "The code has been sent to the email"}
                            )
    return response


@router.post("/check-code")
async def check_code(email: str = Body(),
                     code: str = Body(),
                     db: AsyncSession = Depends(get_db)):
    info_logger.info(f" - START check code")

    if await options_services.check_code(db, email, code):
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={"Success": "Code accepted"}
                            )
    else:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"Error": "Code cancelled"}
                            )


@router.post("/new-password")
async def new_password(new_password: str = Body(),
                       email: str = Body(),
                       db: AsyncSession = Depends(get_db)):
    info_logger.info(f" - START new password")

    if await options_services.new_password(db, new_password, email):
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={"Success": "Password changed"}
                            )
    else:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"Error": "Password not changed"}
                            )
