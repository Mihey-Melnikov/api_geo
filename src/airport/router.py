from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy import update, select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.airport.models import airport
from src.airport.schemas import AirportCreate, AirportRead, AirportUpdate

router = APIRouter(
    prefix="/airport",
    tags=["Airport"]
)

@router.get("/{id}", response_model=AirportRead)
async def get_airport_by_id(id: int, session: AsyncSession = Depends(get_async_session)):
    """
    Get full information about the city by ID.
    """
    query = select(airport) \
            .where(airport.c.id == id, airport.c.deleted_at.is_(None))
    result = await session.execute(query)
    return result.one_or_none()

@router.get("/", response_model=List[AirportRead])
async def get_all_cities(session: AsyncSession = Depends(get_async_session)):
    """
    Get full information on all cities.
    """
    query = select(airport) \
            .where(airport.c.deleted_at.is_(None)) \
            .order_by(airport.c.id)
    result = await session.execute(query)
    return result.mappings().all()

@router.post("/", response_model=AirportRead)
async def add_airporty(new_airport: AirportCreate, session: AsyncSession = Depends(get_async_session)):
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
async def delete_airport(id: int, session: AsyncSession = Depends(get_async_session)):
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
async def update_airport(id: int, updated_rows: AirportUpdate, session: AsyncSession = Depends(get_async_session)):
    """
    Change the airport.
    """
    query = update(airport) \
            .where(airport.c.id == id, airport.c.deleted_at.is_(None)) \
            .values(updated_rows.model_dump(exclude_unset=True)) \
            .returning(airport)
    result = await session.execute(query)
    await session.commit()
    return result.one_or_none()