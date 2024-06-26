from datetime import datetime
import math
from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, update, select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.metro.models import metro
from src.region.models import region
from src.city.models import city
from src.metro.schemas import MetroCreate, MetroRead, MetroSearch, MetroUpdate
from src.translate.models import translate

router = APIRouter(
    prefix="/api/metro",
    tags=["Metro"]
)

@router.get("/{id}", response_model=MetroRead)
async def get_metro_by_id(
    id: int,
    session: AsyncSession = Depends(get_async_session)):
    """
    Get full information about the metro by ID.
    """
    query = select(metro) \
            .where(metro.c.id == id)
    result = await session.execute(query)
    return result.one_or_none()

@router.get("/", response_model=MetroSearch)
async def search_metro(
    term: str | None = None,
    country_id: int | None = None,
    region_id: int | None = None,
    city_id: int | None = None,
    include_deleted: bool | None = False,
    page_number: int = Query(ge=1, default=1), 
    page_size: int = Query(ge=1, le=100, default=100),
    session: AsyncSession = Depends(get_async_session)):
    """
    Search metro by station name. Or get information about all metros.
    """
    ids = []
    if term is not None:
        query = select(translate.c.entity_id) \
                .where(translate.c.entity == 'metro',
                       func.lower(translate.c.translate).like(func.lower(f"%{term}%")))
        result = await session.execute(query)
        ids = [item["entity_id"] for item in result.mappings().all()]
        
    query = select(metro) \
            .join(city, city.c.id == metro.c.city_id) \
            .join(region, region.c.id == city.c.region_id) \
            .where(
                metro.c.id.in_(ids) if term else True,
                metro.c.city_id == city_id if city_id else True,
                city.c.region_id == region_id if region_id else True,
                region.c.country_id == country_id if country_id else True,
                metro.c.deleted_at.is_(None) if not include_deleted else True) \
            .order_by(metro.c.id)
    result = await session.execute(query)
    data = result.mappings().all()
    return {"data": data[(page_number - 1) * page_size:page_number * page_size], "pagination": {
            "page_number": page_number,
            "page_size": page_size,
            "total_pages": math.ceil(len(data) / page_size),
        }}

@router.post("/", response_model=MetroRead)
async def add_metro(
    new_metro: MetroCreate,
    session: AsyncSession = Depends(get_async_session)):
    """
    Create a new metro.
    """
    query = insert(metro) \
            .values(new_metro.model_dump()) \
            .returning(metro)
    result = await session.execute(query)
    await session.commit()
    return result.one_or_none()

@router.delete("/{id}", response_model=MetroRead)
async def delete_city(
    id: int,
    session: AsyncSession = Depends(get_async_session)):
    """
    Delete a metro.
    """
    query = update(metro) \
            .where(metro.c.id == id) \
            .values(deleted_at=datetime.now()) \
            .returning(metro)
    result = await session.execute(query)
    await session.commit()
    return result.one_or_none()

@router.patch("/{id}", response_model=MetroRead)
async def update_metro(
    id: int,
    updated_rows: MetroUpdate, 
    session: AsyncSession = Depends(get_async_session)):
    """
    Change the metro.
    """
    query = update(metro) \
            .where(metro.c.id == id) \
            .values(updated_rows.model_dump(exclude_unset=True)) \
            .returning(metro)
    result = await session.execute(query)
    await session.commit()
    return result.one_or_none()
