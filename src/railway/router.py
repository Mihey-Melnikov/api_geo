from datetime import datetime
import math
from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy import func, or_, update, select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from logger.logger import get_api_logger
from src.railway.models import railway
from src.railway.schemas import RailwayCreate, RailwayRead, RailwayUpdate, RailwaySearch
from src.translate.models import translate


router = APIRouter(
    prefix="/api/railway",
    tags=["Railway"]
)

@router.get("/{id}", response_model=RailwayRead)
async def get_railway_by_id(
    request: Request,
    id: int,
    session: AsyncSession = Depends(get_async_session)):
    """
    Get full information about the railway station by ID.
    """
    query = select(railway) \
            .where(railway.c.id == id)
    result = await session.execute(query)
    data = result.one_or_none()
    logger = get_api_logger(str(request.url))
    logger.info(data)
    return data

@router.get("/", response_model=RailwaySearch)
async def search_railway(
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
    Search railway by name and express3 code. Or get information about all railways.
    """
    ids = []
    if term is not None:
        query = select(translate.c.entity_id) \
                .where(translate.c.entity == 'railway', 
                       func.lower(translate.c.translate).like(func.lower(f"%{term}%")))
        result = await session.execute(query)
        ids = [item["entity_id"] for item in result.mappings().all()]

    query = select(railway) \
            .where(or_(
                    railway.c.express3_code.like(f"%{term}%") if term else True,
                    railway.c.id.in_(ids) if term else True),
                railway.c.city_id == int(city_id) if city_id else True,
                railway.c.region_id == int(region_id) if region_id else True,
                railway.c.country_id == int(country_id) if country_id else True,
                railway.c.deleted_at.is_(None) if not include_deleted else True) \
            .order_by(railway.c.id)
    result = await session.execute(query)
    data = result.mappings().all()
    logger = get_api_logger(str(request.url))
    return data
    return {"data": data[(page_number - 1) * page_size:page_number * page_size], "pagination": {
            "page_number": page_number,
            "page_size": page_size,
            "total_pages": math.ceil(len(data) / page_size),
        }}

@router.post("/", response_model=RailwayRead)
async def add_railway(
    request: Request,
    new_railway: RailwayCreate,
    session: AsyncSession = Depends(get_async_session)):
    """
    Create a new railway station.
    """
    query = insert(railway) \
            .values(new_railway.model_dump()) \
            .returning(railway)
    result = await session.execute(query)
    await session.commit()
    data = result.one_or_none()
    logger = get_api_logger(str(request.url))
    logger.info(data)
    return data

@router.delete("/{id}", response_model=RailwayRead)
async def delete_railway(
    request: Request,
    id: int,
    session: AsyncSession = Depends(get_async_session)):
    """
    Delete a railway station.
    """
    query = update(railway) \
            .where(railway.c.id == id) \
            .values(deleted_at=datetime.now()) \
            .returning(railway)
    result = await session.execute(query)
    await session.commit()
    data = result.one_or_none()
    logger = get_api_logger(str(request.url))
    logger.info(data)
    return data

@router.patch("/{id}", response_model=RailwayRead)
async def update_railway(
    request: Request,
    id: int,
    updated_rows: RailwayUpdate,
    session: AsyncSession = Depends(get_async_session)):
    """
    Change the railway station.
    """
    query = update(railway) \
            .where(railway.c.id == id) \
            .values(updated_rows.model_dump(exclude_unset=True)) \
            .returning(railway)
    result = await session.execute(query)
    await session.commit()
    data = result.one_or_none()
    logger = get_api_logger(str(request.url))
    logger.info(data)
    return data
