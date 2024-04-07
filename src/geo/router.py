from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy import update, select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.geo.models import city
from src.geo.schemas import CityCreate, CityUpdate

router = APIRouter(
    prefix="/geo",
    tags=["Geography"]
)

@router.get("/city/{id}")
async def get_city_by_id(id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(city).where(city.c.id == id and city.c.deleted_at is not None)
    result = await session.execute(query)
    return result.mappings().all()

@router.get("/cities")
async def get_all_cities(session: AsyncSession = Depends(get_async_session)):
    query = select(city).where(city.c.deleted_at is not None)
    result = await session.execute(query)
    return result.mappings().all()

@router.post("/city")
async def add_city(new_city: CityCreate, session: AsyncSession = Depends(get_async_session)):
    query = insert(city).values(**new_city.model_dump()).returning(city)
    result = await session.execute(query)
    await session.commit()
    return result.mappings().all()

@router.put("/city/{id}")
async def update_city(updated_rows: CityUpdate, session: AsyncSession = Depends(get_async_session)):
    pass

@router.delete("/city/{id}")
async def delete_city(id: int, session: AsyncSession = Depends(get_async_session)):
    query = update(city).where(city.c.id == id).values(deleted_at=datetime.now()).returning(city)
    result = await session.execute(query)
    await session.commit()
    return result.mappings().all()

