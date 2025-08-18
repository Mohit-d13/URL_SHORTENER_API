import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from datetime import timedelta

from app.config import settings
from app.database import get_session
from app.main import app
from app.models import User, Site
from app.auth import create_access_token
from app.utils import get_hash_password

# Sepreate database session for testing api route
@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

# Override main session with our new test session and creating testclient instance
@pytest.fixture(name="client")
def get_client_fixture(session: Session):
    def get_session_override():
        return session
    
    app.dependency_overrides[get_session] = get_session_override
    
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

# Create Multiple Users
def create_user_factory(session: Session, _username_: str, _email_: str, _password_: str):
    user = User(username=_username_, email=_email_, password=get_hash_password(_password_))
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

# Creates dummy user 1 for tests
@pytest.fixture(name="dummy_user1")
def dummy_user1_fixture(session: Session):
    dummy_user = create_user_factory(session, "Aporva001", "Aporvanayar001@gmail.com", "nanobots")
    return dummy_user

# Generate access token for authorized_clients
def grant_access_token(user: User):
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    return access_token

# Creates Authorized client 1
@pytest.fixture(name="authorized_client1")
def authorized_client1_fixture(client: TestClient, dummy_user1: User):
    access_token = grant_access_token(dummy_user1)
    client.headers.update({"Authorization": f"Bearer {access_token}"})
    yield client
    client.headers.clear()

# Creates url for testing
@pytest.fixture(name="sample_url")
def sample_url_fixture(dummy_user1: User, session: Session):
    url_data = Site(target_url="https://www.youtube.com/watch?v=NhDYbskXRgc&t=4886s", url_key="9dke7e", user=dummy_user1)
    session.add(url_data)
    session.commit()
    session.refresh(url_data)
    return url_data

# Creates at list url links data for testing
@pytest.fixture(name="sample_urls_list")
def sample_urls_list_fixture(dummy_user1: User, session: Session):
    urls = [
        Site(target_url="https://www.youtube.com/watch?v=NhDYbskXRgc&t=4886s", url_key="9dke7e", user=dummy_user1),
        Site(target_url="https://www.youtube.com/watch?v=j9QmMEWmcfo", url_key="dd3jy8r", user=dummy_user1)
    ]

    session.add_all(urls)
    session.commit()

    for url in urls:
        session.refresh(url)

    return urls
