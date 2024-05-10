from datetime import datetime
from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, MetaData
from src.database import metadata

language = Table("language", metadata,
    Column("language_iso639", String(2), primary_key=True, index=True),
    Column("description", String, nullable=False),
)

translate = Table("translate", metadata,
    Column("entity", String, nullable=False, primary_key=True),
    Column("entity_id", Integer, nullable=False, primary_key=True, index=True),
    Column("language", String(2), nullable=False, primary_key=True, index=True),
    Column("translate", String, nullable=False, index=True),
    Column("last_updated_at", TIMESTAMP, default=datetime.now, onupdate=datetime.now, nullable=False),
)