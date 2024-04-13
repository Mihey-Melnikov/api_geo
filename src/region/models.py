from datetime import datetime
from sqlalchemy import Boolean, ForeignKey, Table, Column, Integer, String, TIMESTAMP, MetaData
from src.country.models import country

metadata = MetaData()

region = Table("region", metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("country_id", Integer, ForeignKey(country.c.id), nullable=False),
    Column("name", String, nullable=False),
    Column("osm_id", Integer, nullable=False),
    Column("osm_type", String(1), nullable=False),
    Column("last_updated_at", TIMESTAMP, default=datetime.now, onupdate=datetime.now, nullable=False),
    Column("deleted_at", TIMESTAMP, default=None, nullable=True),
    Column("need_automatic_update", Boolean, default=True),
)