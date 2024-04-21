from datetime import datetime
from typing import List
from pydantic import BaseModel

class Pagination(BaseModel):
    page_number: int
    page_size: int
    total_pages: int

class MetroRead(BaseModel):
    id: int
    city_id: int
    station_name: str
    line_name: str
    latitude: float
    longitude: float
    osm_id: int
    osm_type: str
    need_automatic_update: bool | None = True
    last_updated_at: datetime
    deleted_at: datetime | None

class MetroSearch(BaseModel):
    data: List[MetroRead]
    pagination: Pagination

class MetroCreate(BaseModel):
    city_id: int
    station_name: str
    line_name: str
    latitude: float
    longitude: float
    osm_id: int
    osm_type: str
    need_automatic_update: bool | None = True

class MetroUpdate(BaseModel):
    city_id: int | None = None
    station_name: str | None = None
    line_name: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    osm_id: int | None = None
    osm_type: str | None = None
    need_automatic_update: bool | None = None
    deleted_at: datetime | None = None