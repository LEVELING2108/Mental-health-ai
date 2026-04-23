from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from api.schemas.user import TokenData
from core.config import settings
from core.database import get_db
from db.models import User


def get_current_user(token: str = Depends(lambda: None), db: Session = Depends(get_db)):
    """In production, replace with OAuth2PasswordBearer."""
    # Note: We are making token optional for backwards compatibility,
    # but strictly checking it when required for history routes.
    from fastapi.security import OAuth2PasswordBearer
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.email == token_data.email).first()
    if user is None:
        raise credentials_exception
    return user

def get_current_user_optional(token: str = Depends(lambda: None), db: Session = Depends(get_db)):
    """Optional dependency for routes that can be used anonymously (like predict)"""
    if not token:
        return None
    try:
        # Try to parse it manually if it exists
        return get_current_user(token, db)
    except:
        return None
