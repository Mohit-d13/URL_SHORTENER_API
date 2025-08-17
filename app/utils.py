import bcrypt
from random import choices
import string
from user_agents import parse
from sqlmodel import select
from .models import User

# Return decode str hashed password with bcrypt algo from password in binary and rand salt
def get_hash_password(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

def generate_unique_key(length):
    return ''.join(choices(string.ascii_letters + string.digits, k=length))

def get_browser_info(user_agent_str):
    ua = parse(user_agent_str)

def get_user_from_db(username: str, session):
    statement = select(User).where(User.username == username)
    user = session.exec(statement).one_or_none()
    return user
