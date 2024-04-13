from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy import update, select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.geo.models import city
from src.geo.schemas import CityCreate, CityUpdate, CityRead

router = APIRouter(
    prefix="/city",
    tags=["City"]
)

@router.get("/{id}", response_model=CityRead)
async def get_city_by_id(id: int, session: AsyncSession = Depends(get_async_session)):
    """
    Get full information about the city by ID.
    """
    query = select(city) \
            .where(city.c.id == id, city.c.deleted_at.is_(None))
    result = await session.execute(query)
    return result.one_or_none()

@router.get("/", response_model=List[CityRead])
async def get_all_cities(session: AsyncSession = Depends(get_async_session)):
    """
    Get full information on all cities.
    """
    query = select(city) \
            .where(city.c.deleted_at.is_(None)) \
            .order_by(city.c.id)
    result = await session.execute(query)
    return result.mappings().all()

@router.post("/", response_model=CityRead)
async def add_city(new_city: CityCreate, session: AsyncSession = Depends(get_async_session)):
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
async def delete_city(id: int, session: AsyncSession = Depends(get_async_session)):
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
async def update_city(id: int, updated_rows: CityUpdate, session: AsyncSession = Depends(get_async_session)):
    """
    Change the city.
    """
    query = update(city) \
            .where(city.c.id == id, city.c.deleted_at.is_(None)) \
            .values(updated_rows.model_dump(exclude_unset=True)) \
            .returning(city)
    result = await session.execute(query)
    await session.commit()
    return result.one_or_none()