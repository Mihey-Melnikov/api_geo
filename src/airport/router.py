import math
from datetime import datetime
from fastapi import APIRouter, Depends, Query
from sqlalchemy import or_, update, select, insert, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.airport.models import airport
from src.region.models import region
from src.city.models import city
from src.airport.schemas import AirportCreate, AirportRead, AirportSearch, AirportUpdate
from src.translate.models import translation

router = APIRouter(
    prefix="/api/airport",
    tags=["Airport"]
)

@router.get("/{id}", response_model=AirportRead)
async def get_airport_by_id(
    id: int,
    session: AsyncSession = Depends(get_async_session)):
    """
    Get full information about the city by ID.
    """
    query = select(airport) \
            .where(airport.c.id == id)
    result = await session.execute(query)
    return result.one_or_none()

@router.get("/", response_model=AirportSearch)
async def search_airport(
    term: str | None = None,
    country_id: int | None = None,
    region_id: int | None = None,
    city_id: int | None = None,
    include_deleted: bool | None = False,
    page_number: int = Query(ge=1, default=1),
    page_size: int = Query(ge=1, le=100, default=100),
    session: AsyncSession = Depends(get_async_session)):
    """
    Search airports by name and IATA. Or get information about all airports.
    """
    transl_ids = []
    if term:
        query = select(translation.c.entity_id) \
                .where(translation.c.entity == 'airport',
                       func.lower(translation.c.translate).like(func.lower(f"%{term}%")))
        result = await session.execute(query)
        transl_ids = [item["entity_id"] for item in result.mappings().all()]

    query = select(airport) \
            .join(city, city.c.id == airport.c.city_id) \
            .join(region, region.c.id == city.c.region_id) \
            .where(or_(
                    airport.c.iata_en.like(f"%{term}%") if term else True,
                    airport.c.iata_ru.like(f"%{term}%") if term else True,
                    airport.c.id.in_(transl_ids) if term else True
                    ), 
                airport.c.city_id == city_id if city_id else True,
                city.c.region_id == region_id if region_id else True,
                region.c.country_id == country_id if country_id else True,
                airport.c.deleted_at.is_(None) if not include_deleted else True
            ) \
            .order_by(airport.c.id)
    result = await session.execute(query)

    data = result.mappings().all()
    return {"data": data[(page_number - 1) * page_size:page_number * page_size], "pagination": {
            "page_number": page_number,
            "page_size": page_size,
            "total_pages": math.ceil(len(data) / page_size),
        }}

@router.post("/", response_model=AirportRead)
async def add_airport(
    new_airport: AirportCreate,
    session: AsyncSession = Depends(get_async_session)):
    """
    Create a new airport.
    """
    query = insert(airport) \
            .values(new_airport.model_dump()) \
            .returning(airport)
    result = await session.execute(query)
    await session.commit()
    return result.one_or_none()

@router.delete("/{id}", response_model=AirportRead)
async def delete_airport(
    id: int,
    session: AsyncSession = Depends(get_async_session)):
    """
    Delete a airport.
    """
    query = update(airport) \
            .where(airport.c.id == id) \
            .values(deleted_at=datetime.now()) \
            .returning(airport)
    result = await session.execute(query)
    await session.commit()
    return result.one_or_none()

@router.patch("/{id}", response_model=AirportRead)
async def update_airport(
    id: int,
    updated_rows: AirportUpdate,
    session: AsyncSession = Depends(get_async_session)):
    """
    Change the airport.
    """
    query = update(airport) \
            .where(airport.c.id == id) \
            .values(updated_rows.model_dump(exclude_unset=True)) \
            .returning(airport)
    result = await session.execute(query)
    await session.commit()
    return result.one_or_none()
