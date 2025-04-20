from typing import Annotated
from fastapi import Depends
from sqlmodel import SQLModel, Session, create_engine
from .config import settings

postgresql_url = f"postgresql://{settings.db_username}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"

engine = create_engine(postgresql_url)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

# This is a dependency that provides a session to the route handlers.
SessionDep = Annotated[Session, Depends(get_session)]


