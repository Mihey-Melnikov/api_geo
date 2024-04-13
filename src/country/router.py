from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy import update, select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.country.models import country
from src.country.schemas import CountryCreate, CountryRead, CountryUpdate

router = APIRouter(
    prefix="/country",
    tags=["Country"]
)

@router.get("/{id}", response_model=CountryRead)
async def get_country_by_id(id: int, session: AsyncSession = Depends(get_async_session)):
    """
    Get full information about the country by ID.
    """
    query = select(country) \
            .where(country.c.id == id, country.c.deleted_at.is_(None))
    result = await session.execute(query)
    return result.one_or_none()

@router.get("/", response_model=List[CountryRead])
async def get_all_countries(session: AsyncSession = Depends(get_async_session)):
    """
    Get full information on all countries.
    """
    query = select(country) \
            .where(country.c.deleted_at.is_(None)) \
            .order_by(country.c.id)
    result = await session.execute(query)
    return result.mappings().all()

@router.post("/", response_model=CountryRead)
async def add_country(new_country: CountryCreate, session: AsyncSession = Depends(get_async_session)):
    """
    Create a new country.
    """
    query = insert(country) \
            .values(new_country.model_dump()) \
            .returning(country)
    result = await session.execute(query)
    await session.commit()
    return result.one_or_none()

@router.delete("/{id}", response_model=CountryRead)
async def delete_country(id: int, session: AsyncSession = Depends(get_async_session)):
    """
    Delete a country.
    """
    query = update(country) \
            .where(country.c.id == id) \
            .values(deleted_at=datetime.now()) \
            .returning(country)
    result = await session.execute(query)
    await session.commit()
    return result.one_or_none()

@router.patch("/{id}", response_model=CountryRead)
async def update_country(id: int, updated_rows: CountryUpdate, session: AsyncSession = Depends(get_async_session)):
    """
    Change the country.
    """
    query = update(country) \
            .where(country.c.id == id, country.c.deleted_at.is_(None)) \
            .values(updated_rows.model_dump(exclude_unset=True)) \
            .returning(country)
    result = await session.execute(query)
    await session.commit()
    return result.one_or_none()