from datetime import datetime
import math
from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy import func, update, select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from src.region.models import region
from src.region.schemas import RegionRead, RegionCreate, RegionUpdate, RegionSearch
from src.translate.models import translate
from src.logger.logger import get_api_logger


router = APIRouter(
    prefix="/api/region",
    tags=["Region"]
)

@router.get("/{id}", response_model=RegionRead)
async def get_region_by_id(
    request: Request,
    id: int,
    session: AsyncSession = Depends(get_async_session)):
    """
    Get full information about the region by ID.
    """
    query = select(region) \
            .where(region.c.id == id)
    result = await session.execute(query)
    data = result.one_or_none()
    logger = get_api_logger(str(request.url))
    logger.info(data)
    return data

@router.get("/", response_model=RegionSearch)
async def search_regions(
    request: Request,
    term: str | None = None,
    country_id: str | None = None,
    include_deleted: bool | None = False,
    page_number: int = Query(ge=1, default=1),
    page_size: int = Query(ge=1, le=100, default=100),
    session: AsyncSession = Depends(get_async_session)):
    """
    Search regions by name. Or get information about all regions.
    """
    ids = []
    if term is not None:
        query = select(translate.c.entity_id) \
                .where(translate.c.entity == 'region',
                       func.lower(translate.c.translate).like(func.lower(f"%{term}%")))
        result = await session.execute(query)
        ids = [item["entity_id"] for item in result.mappings().all()]

    query = select(region) \
            .where(
                region.c.id.in_(ids) if term else True,
                region.c.country_id == int(country_id) if country_id else True,
                region.c.deleted_at.is_(None) if not include_deleted else True) \
            .order_by(region.c.id)
    result = await session.execute(query)
    data = result.mappings().all()
    logger = get_api_logger(str(request.url))
    logger.info(data)
    return {"data": data[(page_number - 1) * page_size:page_number * page_size], "pagination": {
            "page_number": page_number,
            "page_size": page_size,
            "total_pages": math.ceil(len(data) / page_size),
        }}

@router.post("/", response_model=RegionRead)
async def add_region(
    request: Request,
    new_region: RegionCreate,
    session: AsyncSession = Depends(get_async_session)):
    """
    Create a new region.
    """
    query = insert(region) \
            .values(new_region.model_dump()) \
            .returning(region)
    result = await session.execute(query)
    await session.commit()
    data = result.one_or_none()
    logger = get_api_logger(str(request.url))
    logger.info(data)
    return data

@router.delete("/{id}", response_model=RegionRead)
async def delete_region(
    request: Request,
    id: int,
    session: AsyncSession = Depends(get_async_session)):
    """
    Delete a region.
    """
    query = update(region) \
            .where(region.c.id == id) \
            .values(deleted_at=datetime.now()) \
            .returning(region)
    result = await session.execute(query)
    await session.commit()
    data = result.one_or_none()
    logger = get_api_logger(str(request.url))
    logger.info(data)
    return data

@router.patch("/{id}", response_model=RegionRead)
async def update_region(
    request: Request,
    id: int,
    updated_rows: RegionUpdate,
    session: AsyncSession = Depends(get_async_session)):
    """
    Change the region.
    """
    query = update(region) \
            .where(region.c.id == id) \
            .values(updated_rows.model_dump(exclude_unset=True)) \
            .returning(region)
    result = await session.execute(query)
    await session.commit()
    data = result.one_or_none()
    logger = get_api_logger(str(request.url))
    logger.info(data)
    return data
