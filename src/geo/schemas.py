from datetime import datetime

from pydantic import BaseModel

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
    region_id: int
    country_id: int
    name: str
    iata: str
    timezone: str
    latitude: float
    longitude: float
    osm_id: int
    osm_type: str
    need_automatic_update: bool