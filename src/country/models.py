from datetime import datetime
from sqlalchemy import Boolean, Float, Table, Column, Integer, String, TIMESTAMP, MetaData
from src.database import metadata

country = Table("country", metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("name", String, nullable=False),
    Column("iso3116_alpha2", String(2), nullable=False),
    Column("iso3166_alpha3", String(3), nullable=False),
    Column("phone_code", String, nullable=False),
    Column("phone_mask", String, nullable=False),
    Column("latitude", Float, nullable=False),
    Column("longitude", Float, nullable=False),
    Column("osm_id", String, nullable=False),
    Column("osm_type", String(1), nullable=False),
    Column("last_updated_at", TIMESTAMP, default=datetime.now, onupdate=datetime.now, nullable=False),
    Column("deleted_at", TIMESTAMP, default=None, nullable=True),
    Column("need_automatic_update", Boolean, default=True),
)