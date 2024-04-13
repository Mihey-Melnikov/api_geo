from datetime import datetime
from sqlalchemy import Boolean, Float, ForeignKey, Table, Column, Integer, String, TIMESTAMP, MetaData
from src.city.models import city
from src.region.models import region
from src.country.models import country

metadata = MetaData()

railway = Table("railway_station", metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("express3_code", Integer, nullable=False, index=True),
    Column("is_main", Boolean, nullable=False, default=False),
    Column("city_id", Integer, ForeignKey(city.c.id), nullable=True),
    Column("region_id", Integer, ForeignKey(region.c.id), nullable=True),
    Column("country_id", Integer, ForeignKey(country.c.id), nullable=False),
    Column("name", String, nullable=False),
    Column("timezone", String, nullable=False),
    Column("latitude", Float, nullable=False),
    Column("longitude", Float, nullable=False),
    Column("osm_id", Integer, nullable=False),
    Column("osm_type", String(1), nullable=False),
    Column("last_updated_at", TIMESTAMP, default=datetime.now, onupdate=datetime.now, nullable=False),
    Column("deleted_at", TIMESTAMP, default=None, nullable=True),
    Column("need_automatic_update", Boolean, default=True),
)