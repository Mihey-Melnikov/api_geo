from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy import update, select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.railway.models import railway
from src.railway.schemas import RailwayCreate, RailwayRead, RailwayUpdate

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
async def get_all_railways(session: AsyncSession = Depends(get_async_session)):
    """
    Get full information on all railway stations.
    """
    query = select(railway) \
            .where(railway.c.deleted_at.is_(None)) \
            .order_by(railway.c.id)
    result = await session.execute(query)
    return result.mappings().all()

@router.post("/", response_model=RailwayRead)
async def add_railwayy(new_railway: RailwayCreate, session: AsyncSession = Depends(get_async_session)):
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