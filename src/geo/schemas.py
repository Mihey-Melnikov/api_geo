from datetime import datetime
from typing import Optional

from pydantic import BaseModel

class CityRead(BaseModel):
    id: int
    region_id: int
    country_id: int
    name: str
    iata: str | None = None
    timezone: str
    latitude: float
    longitude: float
    osm_id: int
    osm_type: str
    need_automatic_update: bool | None = True

class CityCreate(BaseModel):
    region_id: int
    country_id: int
    name: str
    iata: str | None = None
    timezone: str
    latitude: float
    longitude: float
    osm_id: int
    osm_type: str
    need_automatic_update: bool | None = True

class CityUpdate(BaseModel):
    region_id: int | None = None
    country_id: int | None = None
    name: str | None = None
    iata: str | None = None
    timezone: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    osm_id: int | None = None
    osm_type: str | None = None
    need_automatic_update: bool | None = None