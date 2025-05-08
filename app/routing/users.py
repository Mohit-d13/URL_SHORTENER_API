from typing import Annotated
from datetime import timedelta
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from ..auth import CurrentUserDep, create_access_token
from ..config import settings 
from ..database import SessionDep
from ..models import User
from ..schemas import UserCreate, UserRead, Token
from .. import utils


router = APIRouter(
    tags=["users"],
)

# signup route for user registration
@router.post("/signup/", status_code=201, response_model=UserRead)
async def signup(user: UserCreate, session: SessionDep):
    if utils.get_user_from_db(user.username, session) is not None:
        raise HTTPException(status_code=400, detail="Username is already registered")
    
    user.password = utils.get_hash_password(user.password)
    user_db = User.model_validate(user)
    session.add(user_db)
    session.commit()
    session.refresh(user_db)
    return user_db

# login route for user authentication
@router.post("/login/")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep) -> Token:
    badrequest_exception = HTTPException(
            status_code=401, 
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
            )
    
    user = utils.get_user_from_db(form_data.username, session)
    if not user:
        raise badrequest_exception
    if not utils.verify_password(form_data.password, user.password):
        raise badrequest_exception
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

# get self profile information
@router.get("/users/me/", response_model=UserRead)
async def read_users_me(current_user: CurrentUserDep):
    return current_user
    