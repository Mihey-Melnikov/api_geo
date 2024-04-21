from datetime import datetime
from sqlalchemy import Boolean, Float, ForeignKey, Table, Column, Integer, String, TIMESTAMP
from src.city.models import city
from src.database import metadata

airport = Table("airport", metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("city_id", Integer, ForeignKey(city.c.id), nullable=False),
    Column("name", String, nullable=False),
    Column("iata_en", String(3), nullable=True, index=True),
    Column("iata_ru", String(3), nullable=True, index=True),
    Column("timezone", String, nullable=False),
    Column("latitude", Float, nullable=False),
    Column("longitude", Float, nullable=False),
    Column("osm_id", Integer, nullable=False),
    Column("osm_type", String(1), nullable=False),
    Column("last_updated_at", TIMESTAMP, default=datetime.now, onupdate=datetime.now, nullable=False),
    Column("deleted_at", TIMESTAMP, default=None, nullable=True),
    Column("need_automatic_update", Boolean, default=True),
)