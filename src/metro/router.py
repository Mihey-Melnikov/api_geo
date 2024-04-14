from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy import func, update, select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.metro.models import metro
from src.metro.schemas import MetroCreate, MetroRead, MetroUpdate
from src.translate.models import translation

router = APIRouter(
    prefix="/metro",
    tags=["Metro"]
)

@router.get("/{id}", response_model=MetroRead)
async def get_metro_by_id(id: int, session: AsyncSession = Depends(get_async_session)):
    """
    Get full information about the metro by ID.
    """
    query = select(metro) \
            .where(metro.c.id == id, metro.c.deleted_at.is_(None))
    result = await session.execute(query)
    return result.one_or_none()

@router.get("/", response_model=List[MetroRead])
async def search_metro(term: str | None = None, session: AsyncSession = Depends(get_async_session)):
    """
    Search metro by station name. Or get information about all metros.
    """
    ids = []
    if term is not None:
        query = select(translation.c.entity_id) \
                .where(translation.c.entity == 'metro', 
                       func.lower(translation.c.translate).like(func.lower(f"%{term}%")))
        result = await session.execute(query)
        ids = [item["entity_id"] for item in result.mappings().all()]
        
    query = select(metro) \
            .where(metro.c.deleted_at.is_(None), metro.c.id.in_(ids) if term else True) \
            .order_by(metro.c.id)
    result = await session.execute(query)
    return result.mappings().all()

@router.post("/", response_model=MetroRead)
async def add_metro(new_metro: MetroCreate, session: AsyncSession = Depends(get_async_session)):
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
async def delete_city(id: int, session: AsyncSession = Depends(get_async_session)):
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
async def update_metro(id: int, updated_rows: MetroUpdate, session: AsyncSession = Depends(get_async_session)):
    """
    Change the metro.
    """
    query = update(metro) \
            .where(metro.c.id == id, metro.c.deleted_at.is_(None)) \
            .values(updated_rows.model_dump(exclude_unset=True)) \
            .returning(metro)
    result = await session.execute(query)
    await session.commit()
    return result.one_or_none()