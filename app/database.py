from typing import Annotated
from fastapi import Depends
from sqlmodel import SQLModel, Session, create_engine
from .config import DATABASE_URL

engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

# This is a dependency that provides a session to the route handlers.
SessionDep = Annotated[Session, Depends(get_session)]


