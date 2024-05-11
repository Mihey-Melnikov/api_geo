import math
from datetime import datetime
from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy import or_, update, select, insert, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from src.airport.models import airport
from src.logger.logger import get_api_logger
from src.region.models import region
from src.city.models import city
from src.airport.schemas import AirportCreate, AirportRead, AirportSearch, AirportUpdate
from src.translate.models import translate

router = APIRouter(
    prefix="/api/airport",
    tags=["Airport"]
)

@router.get("/{id}", response_model=AirportRead)
async def get_airport_by_id(
    request: Request,
    id: int,
    session: AsyncSession = Depends(get_async_session)):
    """
    Get full information about the city by ID.
    """
    query = select(airport) \
            .where(airport.c.id == id)
    result = await session.execute(query)
    data = result.one_or_none()
    logger = get_api_logger(str(request.url))
    logger.info(data)
    return data

@router.get("/", response_model=AirportSearch)
async def search_airport(
    request: Request,
    term: str | None = None,
    country_id: str | None = None,
    region_id: str | None = None,
    city_id: str | None = None,
    include_deleted: bool | None = False,
    page_number: int = Query(ge=1, default=1),
    page_size: int = Query(ge=1, le=100, default=100),
    session: AsyncSession = Depends(get_async_session)):
    """
    Search airports by name and IATA. Or get information about all airports.
    """
    transl_ids = []
    if term:
        query = select(translate.c.entity_id) \
                .where(translate.c.entity == 'airport',
                       func.lower(translate.c.translate).like(func.lower(f"%{term}%")))
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
                airport.c.city_id == int(city_id) if city_id else True,
                city.c.region_id == int(region_id) if region_id else True,
                region.c.country_id == int(country_id) if country_id else True,
                airport.c.deleted_at.is_(None) if not include_deleted else True
            ) \
            .order_by(airport.c.id)
    result = await session.execute(query)

    data = result.mappings().all()
    logger = get_api_logger(str(request.url))
    logger.info(data)
    return {"data": data[(page_number - 1) * page_size:page_number * page_size], "pagination": {
            "page_number": page_number,
            "page_size": page_size,
            "total_pages": math.ceil(len(data) / page_size),
        }}

@router.post("/", response_model=AirportRead)
async def add_airport(
    request: Request,
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
    data = result.one_or_none()
    logger = get_api_logger(str(request.url))
    logger.info(data)
    return data

@router.delete("/{id}", response_model=AirportRead)
async def delete_airport(
    request: Request,
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
    data = result.one_or_none()
    logger = get_api_logger(str(request.url))
    logger.info(data)
    return data

@router.patch("/{id}", response_model=AirportRead)
async def update_airport(
    request: Request,
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
    data = result.one_or_none()
    logger = get_api_logger(str(request.url))
    logger.info(data)
    return data
