from typing import Annotated
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import InvalidTokenError

from .config import settings
from .database import SessionDep
from .schemas import UserRead, TokenData
from .models import User
from .utils import get_user_from_db


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login/")
 
# create access token for user
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

# get current user from token, decode token, check if user exists in db     
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: SessionDep) -> UserRead:
    credantials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username = payload.get("sub")
        if username is None:
            raise credantials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credantials_exception
    user = get_user_from_db(token_data.username, session)
    
    if not user:
        raise credantials_exception
    return user

# get current active user
async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if not current_user.active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# This is a dependency that provides the current active user to the route handlers.
CurrentUserDep = Annotated[User, Depends(get_current_active_user)]

