from datetime import datetime
from pydantic import BaseModel

class AirportRead(BaseModel):
    id: int
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