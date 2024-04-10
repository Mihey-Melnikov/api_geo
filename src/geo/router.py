from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
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
    try:
        query = select(city).where(city.c.id == id and city.c.deleted_at is not None)
        result = await session.execute(query)
        return result.mappings().all()
    except:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None,
        }) 

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

@router.delete("/city/{id}")
async def delete_city(id: int, session: AsyncSession = Depends(get_async_session)):
    query = update(city).where(city.c.id == id).values(deleted_at=datetime.now()).returning(city)
    result = await session.execute(query)
    await session.commit()
    return result.mappings().all()

"""
@router.patch("/city/{id}", response_model=CityUpdate)
async def update_city(id: int, updated_rows: CityUpdate, session: AsyncSession = Depends(get_async_session)) -> City:
    async with session.begin():
        query = select(city).options(selectinload(city)).where(city.c.id == id, city.c.deleted_at.is_(None))
        result = await session.execute(query)
        city_for_update = result.scalars().one_or_none()
        if city_for_update is None:
            raise HTTPException(status_code=404, detail="City not found")
        update_data = updated_rows.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(city_for_update, key, value)
        session.add(city_for_update)
        await session.commit()
        return city_for_update
"""

@router.patch("/city/{id}", response_model=CityUpdate)
async def update_city(id: int, updated_rows: CityUpdate, session: AsyncSession = Depends(get_async_session)):
    query = select(city).where(city.c.id == id, city.c.deleted_at.is_(None))
    result = await session.execute(query)
    city_for_update = result.one_or_none()
    updated_rows.model_dump(exclude_unset=True)
    for name, value in updated_rows.model_dump(exclude_unset=True).items():
        setattr(city_for_update, name, value)
    await session.commit()
    return city_for_update