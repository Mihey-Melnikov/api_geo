from typing import List
from sqlalchemy import Table, func, insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import engine
from src.country.models import country


async def insert_data(data_list: List, model: Table):
    """
    Method for insert data from OSM to DB.
    """
    async with AsyncSession(engine) as session:
        async with session.begin():
            for data in data_list:
                await session.execute(insert(model).values(**data))
        await session.commit()


async def try_get_country_id(country_code: str):
    """
    Try get country id by iso3116_alpha2 country code.
    """
    country_id = None
    async with AsyncSession(engine) as session:
        async with session.begin():
            result = await session.execute(
                select(country) \
                .where(func.lower(country.c.iso3116_alpha2).like(func.lower(f"%{country_code}%")), country.c.deleted_at.is_(None)))
            data = result.mappings().all()
            if data:
                country_id = data[0]["id"]
    return country_id
