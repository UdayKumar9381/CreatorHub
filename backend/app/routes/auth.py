from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from jose import jwt, JWTError
from datetime import datetime, timedelta
from ..core.database import get_db
from ..core.security import get_password_hash, verify_password, create_access_token, create_reset_token
from ..models.models import User
from ..schemas.schemas import UserSignup, UserLogin, Token, UserOut, ForgotPasswordRequest, ResetPasswordRequest
from ..core.config import settings
from ..core.email_utils import send_reset_email
from ..core.constants import (
    ERROR_MSG_EMAIL_TAKEN, 
    ERROR_MSG_INVALID_CREDENTIALS, 
    ERROR_MSG_INVALID_TOKEN, 
    ERROR_MSG_INVALID_TOKEN_TYPE,
    ERROR_MSG_USER_NOT_FOUND
)
from ..core.enums import TokenType

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=UserOut)
async def signup(user_data: UserSignup, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user_data.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail=ERROR_MSG_EMAIL_TAKEN)
    
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password_hash=get_password_hash(user_data.password)
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

import traceback
import logging

logger = logging.getLogger("api")

@router.post("/login", response_model=Token)
async def login(user_data: UserLogin, db: AsyncSession = Depends(get_db)):
    try:
        logger.info(f"LOGIN ATTEMPT: {user_data.email}")
        result = await db.execute(select(User).where(User.email == user_data.email))
        user = result.scalar_one_or_none()
        
        if not user:
            logger.warning(f"LOGIN FAILED: User not found - {user_data.email}")
            raise HTTPException(status_code=401, detail=ERROR_MSG_INVALID_CREDENTIALS)
            
        if not verify_password(user_data.password, user.password_hash):
            logger.warning(f"LOGIN FAILED: Invalid password - {user_data.email}")
            raise HTTPException(status_code=401, detail=ERROR_MSG_INVALID_CREDENTIALS)
        
        access_token = create_access_token(subject=user.id)
        logger.info(f"LOGIN SUCCESS: {user_data.email}")
        return {"access_token": access_token, "token_type": "bearer"}
        
    except HTTPException as he:
        # Re-raise HTTPExceptions as they are intended for the client
        raise he
    except Exception as e:
        # Log the full traceback for any unexpected error
        logger.error(f"CRITICAL LOGIN ERROR for {user_data.email}: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=500, 
            detail=f"Internal Server Error during login: {type(e).__name__}: {str(e)}"
        )

@router.post("/forgot-password")
async def forgot_password(request: ForgotPasswordRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == request.email))
    user = result.scalar_one_or_none()
    
    if user:
        token = create_reset_token(user.email)
        await send_reset_email(user.email, token)
        
    return {"message": "If an account exists with this email, a reset link has been sent."}

@router.post("/reset-password")
async def reset_password(request: ResetPasswordRequest, db: AsyncSession = Depends(get_db)):
    try:
        payload = jwt.decode(request.token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("type") != TokenType.RESET:
            raise HTTPException(status_code=400, detail=ERROR_MSG_INVALID_TOKEN_TYPE)
        email = payload.get("sub")
    except (JWTError, ValueError):
        raise HTTPException(status_code=400, detail=ERROR_MSG_INVALID_TOKEN)
        
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail=ERROR_MSG_USER_NOT_FOUND)
        
    user.password_hash = get_password_hash(request.new_password)
    await db.commit()
    
    return {"message": "Password updated successfully"}

