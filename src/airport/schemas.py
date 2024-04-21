from datetime import datetime
from msilib import schema
from typing import List
from pydantic import BaseModel, Field

class Pagination(BaseModel):
    page_number: int
    page_size: int
    total_pages: int

class AirportRead(BaseModel):
    id: int = Field(..., description="Уникльный идентификатор", example=1)
    city_id: int
    name: str
    iata_en: str | None = None
    iata_ru: str | None = None
    timezone: str
    latitude: float
    longitude: float
    osm_id: int
    osm_type: str
    need_automatic_update: bool | None = True
    last_updated_at: datetime
    deleted_at: datetime | None = None

class AirportSearch(BaseModel):
    data: List[AirportRead]
    pagination: Pagination

class AirportCreate(BaseModel):
    city_id: int
    name: str
    iata_en: str | None = None
    iata_ru: str | None = None
    timezone: str
    latitude: float
    longitude: float
    osm_id: int
    osm_type: str
    need_automatic_update: bool | None = True

class AirportUpdate(BaseModel):
    city_id: int | None = None
    name: str | None = None
    iata_en: str | None = None
    iata_ru: str | None = None
    timezone: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    osm_id: int | None = None
    osm_type: str | None = None
    need_automatic_update: bool | None = None
    deleted_at: datetime | None = None