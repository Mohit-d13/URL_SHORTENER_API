from typing import Annotated, List
from fastapi import APIRouter, HTTPException, Request, Query
from fastapi.responses import RedirectResponse
from sqlmodel import select

from ..auth import CurrentUserDep
from ..database import SessionDep
from ..models import Site, Click
from ..schemas import SiteCreate, SiteRead
from ..utils import generate_unique_key, get_browser_info


router = APIRouter(
    prefix='/urls',
    tags=["sites"],
)

# Create shorten url key
@router.post("/", status_code=201, response_model=SiteRead)
def create_url(url: SiteCreate, session: SessionDep, current_user: CurrentUserDep):
    while True:
        unique_key = generate_unique_key(url.length)
        if session.get(Site, unique_key) is None:
            break
    
    statement = select(Site).where(Site.target_url == url.target_url, Site.user_id == current_user.id)         
    existing_site = session.exec(statement).first()
    if existing_site:
        raise HTTPException(status_code=400, detail="URL already exists in your database.")
    
    data = Site(target_url=url.target_url, url_key=unique_key, user_id=current_user.id)
    session.add(data)
    session.commit()
    session.refresh(data)
    return data


# Get all sites created by user
@router.get("/all/", response_model=List[SiteRead])
def read_all_sites(
    session: SessionDep,
    current_user: CurrentUserDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
    ):
    statement = select(Site).where(Site.user_id == current_user.id).offset(offset).limit(limit)
    data = session.exec(statement).all()
    if not data:
        raise HTTPException(status_code=404, detail="No URLs found")
    
    return data

# Get sites data analytics by url_key
@router.get("/info/{url_key}/", response_model=SiteRead)
def get_url_info(url_key: str, session: SessionDep, current_user: CurrentUserDep):
    data = session.get(Site, url_key)
    if not data:
        raise HTTPException(status_code=404, detail="URL not found")
    
    return SiteRead(
        target_url=data.target_url,
        url_key=data.url_key,
        created_at=data.created_at,
        total_clicks=len(data.clicks),
        clicks_detail=[
            {
                "id": click.id,
                "timestamp": click.timestamp,
                "browser": get_browser_info(click.user_agent)
                }
            for click in data.clicks],
        user=current_user
        )

# returns original website url with url shorten key
@router.get("/{url_key}/")
def get_target_url(url_key: str, request: Request, session: SessionDep):
    data = session.get(Site, url_key) 
    if not data:
        raise HTTPException(status_code=404, detail="URL not found")
    
    click = Click(url_id=data.url_key, user_agent=request.headers.get("user-agent"))
    session.add(click)
    session.commit()
    
    return RedirectResponse(data.target_url)


# Delete url link
@router.delete("/{url_key}/", status_code=204)
def delete_url(url_key: str, session: SessionDep, current_user: CurrentUserDep):
    data = session.get(Site, url_key)
    if not data:
        raise HTTPException(status_code=404, detail="URL not found")
        
    session.delete(data)
    session.commit()   
    return