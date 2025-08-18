from typing import List
from datetime import datetime
from pydantic import BaseModel
from sqlmodel import Field, SQLModel


#============================= Site Model ============================

class SiteBase(SQLModel):
    target_url: str = Field(nullable=False)
    
class SiteCreate(SiteBase):
    length: int = Field(default=6)
    
class SiteRead(SiteBase):
    url_key: str
    created_at: datetime
    total_clicks: int = Field(default=0)
    clicks_detail: List[dict] = Field(default_factory=list)
    user: "UserBase"

    
#============================= User Model =============================

class UserBase(SQLModel):
    username: str = Field(nullable=False, unique=True)
    email: str = Field(nullable=False, unique=True)
       
class UserCreate(UserBase):
    password: str = Field(nullable=False)

class UserUpdate(BaseModel):
    first_name: str | None = Field(max_length=50, default=None)
    last_name: str | None = Field(max_length=50, default=None)
    
class UserRead(UserBase):
    id: int
    active: bool
    first_name: str | None = Field(max_length=50, default=None)
    last_name: str | None = Field(max_length=50, default=None)
    created_at: datetime
    updated_at: datetime

        
#============================= Token Model =============================
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    username: str | None = None
        
