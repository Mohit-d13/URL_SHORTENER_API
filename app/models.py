from typing import Optional, List
from datetime import datetime, timezone
from sqlmodel import Field, SQLModel, Relationship
from .schemas import SiteBase, UserCreate

def get_utc_now():
    return datetime.now(timezone.utc)


# ============================== Click Database Table  =============================

class Click(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    url_id: str = Field(foreign_key="site.url_key", ondelete="CASCADE") # foreign key
    timestamp: datetime = Field(default_factory=get_utc_now)
    user_agent: str = Field(nullable=False)
    url: Optional["Site"] = Relationship(back_populates="clicks") # one-to-one
    
    
# ============================== Site Database Table  =============================

class Site(SiteBase, table=True):
    url_key: str = Field(nullable=False, primary_key=True)
    user_id: int = Field(foreign_key="user.id", nullable=False, ondelete="CASCADE") # foreign key
    created_at: datetime = Field(default_factory=get_utc_now)
    clicks: List[Click] = Relationship(back_populates="url", cascade_delete=True) # one-to-many
    user: Optional["User"] = Relationship(back_populates="urls") # one-to-one
    
    
# ============================== User Database Table  =============================

class User(UserCreate, table=True):
    id: int | None = Field(default=None, primary_key=True)
    first_name: str | None = Field(max_length=50, default=None)
    last_name: str | None = Field(max_length=50, default=None)
    active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=get_utc_now)
    updated_at: datetime = Field(default_factory=get_utc_now)
    urls: List[Site] = Relationship(back_populates="user", cascade_delete=True) # one-to-many

