from datetime import datetime
import math
from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, update, select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.region.models import region
from src.region.schemas import RegionRead, RegionCreate, RegionUpdate, RegionSearch
from src.translate.models import translation

router = APIRouter(
    prefix="/api/region",
    tags=["Region"]
)

@router.get("/{id}", response_model=RegionRead)
async def get_region_by_id(
    id: int, 
    session: AsyncSession = Depends(get_async_session)):
    """
    Get full information about the region by ID.
    """
    query = select(region) \
            .where(region.c.id == id)
    result = await session.execute(query)
    return result.one_or_none()

@router.get("/", response_model=RegionSearch)
async def search_regions(
    term: str | None = None, 
    page_number: int = Query(ge=1, default=1), 
    page_size: int = Query(ge=1, le=100, default=100),
    session: AsyncSession = Depends(get_async_session)):
    """
    Search regions by name. Or get information about all regions.
    """
    ids = []
    if term is not None:
        query = select(translation.c.entity_id) \
                .where(translation.c.entity == 'region', 
                       func.lower(translation.c.translate).like(func.lower(f"%{term}%")))
        result = await session.execute(query)
        ids = [item["entity_id"] for item in result.mappings().all()]

    query = select(region) \
            .where(region.c.id.in_(ids) if term else True) \
            .order_by(region.c.id)
    result = await session.execute(query)
    data = result.mappings().all()
    return {"data": data[(page_number - 1) * page_size:page_number * page_size], "pagination": {
            "page_number": page_number,
            "page_size": page_size,
            "total_pages": math.ceil(len(data) / page_size),
        }}

@router.post("/", response_model=RegionRead)
async def add_region(
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
    return result.one_or_none()

@router.delete("/{id}", response_model=RegionRead)
async def delete_region(
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
    return result.one_or_none()

@router.patch("/{id}", response_model=RegionRead)
async def update_region(
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
    return result.one_or_none()