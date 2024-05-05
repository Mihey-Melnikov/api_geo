from datetime import datetime
import math
from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, or_, update, select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.city.models import city
from src.region.models import region
from src.city.schemas import CityCreate, CityRead, CitySearch, CityUpdate
from src.translate.models import translation

router = APIRouter(
    prefix="/api/city",
    tags=["City"]
)

@router.get("/{id}", response_model=CityRead)
async def get_city_by_id(
    id: int, 
    session: AsyncSession = Depends(get_async_session)):
    """
    Get full information about the city by ID.
    """
    query = select(city) \
            .where(city.c.id == id)
    result = await session.execute(query)
    return result.one_or_none()

@router.get("/", response_model=CitySearch)
async def search_cities(
    term: str | None = None,
    country_id: int | None = None,
    region_id: int | None = None,
    include_deleted: bool | None = False,
    page_number: int = Query(ge=1, default=1), 
    page_size: int = Query(ge=1, le=100, default=100),
    session: AsyncSession = Depends(get_async_session)):
    """
    Search cities by name and IATA. Or get information about all cities.
    """
    ids = []
    if term is not None:
        query = select(translation.c.entity_id) \
                .where(translation.c.entity == 'city', 
                       func.lower(translation.c.translate).like(func.lower(f"%{term}%")))
        result = await session.execute(query)
        ids = [item["entity_id"] for item in result.mappings().all()]

    query = select(city) \
            .join(region, region.c.id == city.c.region_id) \
            .where(or_(
                    city.c.iata.like(f"%{term}%") if term else True,
                    city.c.id.in_(ids) if term else True),
                city.c.region_id == region_id if region_id else True,
                region.c.country_id == country_id if country_id else True,
                region.c.deleted_at.is_(None) if not include_deleted else True) \
            .order_by(city.c.id)
    result = await session.execute(query)
    data = result.mappings().all()
    return {"data": data[(page_number - 1) * page_size:page_number * page_size], "pagination": {
            "page_number": page_number,
            "page_size": page_size,
            "total_pages": math.ceil(len(data) / page_size),
        }}

@router.post("/", response_model=CityRead)
async def add_city(
    new_city: CityCreate, 
    session: AsyncSession = Depends(get_async_session)):
    """
    Create a new city.
    """
    query = insert(city) \
            .values(new_city.model_dump()) \
            .returning(city)
    result = await session.execute(query)
    await session.commit()
    return result.one_or_none()

@router.delete("/{id}", response_model=CityRead)
async def delete_city(
    id: int, 
    session: AsyncSession = Depends(get_async_session)):
    """
    Delete a city.
    """
    query = update(city) \
            .where(city.c.id == id) \
            .values(deleted_at=datetime.now()) \
            .returning(city)
    result = await session.execute(query)
    await session.commit()
    return result.one_or_none()

@router.patch("/{id}", response_model=CityRead)
async def update_city(
    id: int, 
    updated_rows: CityUpdate, 
    session: AsyncSession = Depends(get_async_session)):
    """
    Change the city.
    """
    query = update(city) \
            .where(city.c.id == id) \
            .values(updated_rows.model_dump(exclude_unset=True)) \
            .returning(city)
    result = await session.execute(query)
    await session.commit()
    return result.one_or_none()
