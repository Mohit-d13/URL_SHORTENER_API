from passlib.context import CryptContext
from random import choices
import string
from user_agents import parse
from sqlmodel import select
from .models import User
from .schemas import UserRead


# This is a passlib helper class that provides password hashing and verification with bcrypt algorithm.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_hash_password(password):
    return pwd_context.hash(password)

def generate_unique_key(length):
    return ''.join(choices(string.ascii_letters + string.digits, k=length))

def get_browser_info(user_agent_str):
    ua = parse(user_agent_str)

def get_user_from_db(username: str, session):
    statement = select(User).where(User.username == username)
    user = session.exec(statement).one_or_none()
    return user
