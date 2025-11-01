from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core.config import settings
from app.core.security import verify_token
from app.db.session import get_db as get_db_session
from app.models.user import User
from app.schemas.auth import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.api_v1_prefix}/auth/login")


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async for db in get_db_session():
        yield db


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = verify_token(token, credentials_exception)
    user = await db.get(User, token_data.email)  # assuming email is id, but wait, it's filter by email
    # Actually, db.query(User).filter(User.email == token_data.email).first()
    # For async, it's (await db.execute(select(User).where(User.email == token_data.email))).scalar_one_or_none()
    from sqlalchemy import select
    result = await db.execute(select(User).where(User.email == token_data.email))
    user = result.scalar_one_or_none()
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_admin_user(current_user: User = Depends(get_current_active_user)) -> User:
    if current_user.rol != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user


def get_current_operador_user(current_user: User = Depends(get_current_active_user)) -> User:
    if current_user.rol not in ["admin", "operador"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user
