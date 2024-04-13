from datetime import datetime
from sqlalchemy import Boolean, Float, ForeignKey, Table, Column, Integer, String, TIMESTAMP, MetaData
from src.region.models import region
from src.country.models import country

metadata = MetaData()

city = Table("city", metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("region_id", Integer, ForeignKey(region.c.id), nullable=True),
    Column("country_id", Integer, ForeignKey(country.c.id), nullable=False),
    Column("name", String, nullable=False),
    Column("iata", String(3), nullable=True, index=True),
    Column("timezone", String, nullable=False),
    Column("latitude", Float, nullable=False),
    Column("longitude", Float, nullable=False),
    Column("osm_id", Integer, nullable=False),
    Column("osm_type", String(1), nullable=False),
    Column("last_updated_at", TIMESTAMP, default=datetime.now, onupdate=datetime.now, nullable=False),
    Column("deleted_at", TIMESTAMP, default=None, nullable=True),
    Column("need_automatic_update", Boolean, default=True),
)

translation_language = Table("translation_language", metadata,
    Column("language_iso639", String, primary_key=True, index=True),
    Column("description", String, nullable=False),
)