import sys
sys.path.insert(0, 'C:\\Users\\Пользователь\\Desktop\\api_geo')
# todo костыль, нужно разобраться с путями

import csv
from typing import List
from sqlalchemy import Table, func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import engine
from src.country.models import country
from src.region.models import region
from src.city.models import city
from geopy.distance import geodesic as GD


COUNTRY_TAGS = ["country", "island"]
REGION_TAGS = ["state", "county", "province", "district", "region"]
CITY_TAGS = ["city", "town", "village", "hamlet", "isolated_dwelling", "quarter", "neighbourhood", "suburb"]
AIRPORT_TAGS = ["aeroway", "railway"]
RAILWAY_TAGS = ["railway"]


async def insert_data(data_list: List, model: Table):
    """
    Method for insert data from OSM to DB.
    """
    async with AsyncSession(engine) as session:
        async with session.begin():
            for data in data_list:
                await session.execute(insert(model).values(**data))
        await session.commit()


async def update_data(data_list: List, model: Table):
    """
    Method for update data from OSM to DB.
    """
    async with AsyncSession(engine) as session:
        async with session.begin():
            for data in data_list:
                await session.execute(update(model).where(model.c.id == data["id"]).values(iata = data["iata"]))
        await session.commit()


async def try_get_country_id(country_code: str) -> int | None:
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


async def try_get_region_id(address: list[dict]) -> int | None:
    """
    Try get region id by place addresses.
    """
    region_id = None
    address_osm = [str(addr.get("osm_id")) for addr in address if addr.get("osm_id") is not None]
    async with AsyncSession(engine) as session:
        async with session.begin():
            result = await session.execute(
                select(region) \
                .where(region.c.osm_id.in_(address_osm), region.c.deleted_at.is_(None)))
            data = result.mappings().all()
            if data:
                region_id = data[0]["id"]
    return region_id


async def try_get_city_id(address: list[dict], coordinates: list[float]) -> int:
    """
    Try get city id by place addresses or coordinates.
    """
    city_id = None
    address_osm = [str(addr.get("osm_id")) for addr in address if addr.get("osm_id") is not None]
    async with AsyncSession(engine) as session:
        async with session.begin():
            result = await session.execute(
                select(city) \
                .where(city.c.osm_id.in_(address_osm), city.c.deleted_at.is_(None)))
            data = result.mappings().all()

            if data:
                city_id = data[0]["id"]
            else:
                result = await session.execute(select(city).where(city.c.deleted_at.is_(None)))
                cities = result.mappings().all()
                city_id = await get_nearest_city(cities, coordinates)    

    return city_id


async def get_nearest_city(cities, coordinates) -> int:
    """
    Get nearest city by coordinates.
    """
    min_dist = float('inf')
    city_id = None
    for city in cities:
        dist = GD(coordinates[::-1], [city["latitude"], city["longitude"]]).km
        if dist < min_dist:
            city_id = city["id"]
            min_dist = dist
    return city_id


async def try_get_express_by_osm(osm_id: str) -> str | None:
    """
    Try get express3 code of railway by osm id.
    """
    express_code = None
    with open("C:/Users/Пользователь/Desktop/api_geo/osm/daemons/data_to_fill/express.csv", encoding='utf8') as express_file, \
        open("C:/Users/Пользователь/Desktop/api_geo/osm/daemons/data_to_fill/osm2esr.csv", encoding='utf8') as osm2esr_file:
        express_data = csv.DictReader(express_file, delimiter = ";")
        osm2esr_data = csv.DictReader(osm2esr_file, delimiter = ";")
        esr_code = next((row["esr"] for row in osm2esr_data if row["osm_id"] == osm_id), None)
        express_code = next((row["express"] for row in express_data if row["esr"] == esr_code), None) if esr_code else None
    return express_code


async def table_is_empty(model: Table) -> bool:
    """
    Checking the table for emptiness
    """
    is_empty = True
    async with AsyncSession(engine) as session:
        async with session.begin():
            result = await session.execute(select(model))
            data = result.mappings().all()
            is_empty = bool(data)
    return is_empty


async def update_table(model: Table) -> None:
    """
    Upadate all data in table.
    """
    pass
