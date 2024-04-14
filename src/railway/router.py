from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy import func, or_, update, select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.railway.models import railway
from src.railway.schemas import RailwayCreate, RailwayRead, RailwayUpdate
from src.translate.models import translation

router = APIRouter(
    prefix="/railway",
    tags=["Railway"]
)

@router.get("/{id}", response_model=RailwayRead)
async def get_railway_by_id(id: int, session: AsyncSession = Depends(get_async_session)):
    """
    Get full information about the railway station by ID.
    """
    query = select(railway) \
            .where(railway.c.id == id, railway.c.deleted_at.is_(None))
    result = await session.execute(query)
    return result.one_or_none()

@router.get("/", response_model=List[RailwayRead])
async def search_railway(term: str | None = None, session: AsyncSession = Depends(get_async_session)):
    """
    Search railway by name and express3 code. Or get information about all railways.
    """
    ids = []
    if term is not None:
        query = select(translation.c.entity_id) \
                .where(translation.c.entity == 'railway', 
                       func.lower(translation.c.translate).like(func.lower(f"%{term}%")))
        result = await session.execute(query)
        ids = [item["entity_id"] for item in result.mappings().all()]

    query = select(railway) \
            .where(railway.c.deleted_at.is_(None), or_(
                railway.c.express3_code.like(f"%{term}%") if term else True,
                railway.c.id.in_(ids) if term else True
            )) \
            .order_by(railway.c.id)
    result = await session.execute(query)
    return result.mappings().all()

@router.post("/", response_model=RailwayRead)
async def add_railway(new_railway: RailwayCreate, session: AsyncSession = Depends(get_async_session)):
    """
    Create a new railway station.
    """
    query = insert(railway) \
            .values(new_railway.model_dump()) \
            .returning(railway)
    result = await session.execute(query)
    await session.commit()
    return result.one_or_none()

@router.delete("/{id}", response_model=RailwayRead)
async def delete_railway(id: int, session: AsyncSession = Depends(get_async_session)):
    """
    Delete a railway station.
    """
    query = update(railway) \
            .where(railway.c.id == id) \
            .values(deleted_at=datetime.now()) \
            .returning(railway)
    result = await session.execute(query)
    await session.commit()
    return result.one_or_none()

@router.patch("/{id}", response_model=RailwayRead)
async def update_railway(id: int, updated_rows: RailwayUpdate, session: AsyncSession = Depends(get_async_session)):
    """
    Change the railway station.
    """
    query = update(railway) \
            .where(railway.c.id == id, railway.c.deleted_at.is_(None)) \
            .values(updated_rows.model_dump(exclude_unset=True)) \
            .returning(railway)
    result = await session.execute(query)
    await session.commit()
    return result.one_or_none()