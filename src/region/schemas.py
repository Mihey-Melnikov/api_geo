from datetime import datetime
from typing import List
from pydantic import BaseModel

class Pagination(BaseModel):
    page_number: int
    page_size: int
    total_pages: int

class RegionRead(BaseModel):
    id: int
    country_id: int
    name: str
    latitude: float
    longitude: float
    osm_id: str
    osm_type: str
    need_automatic_update: bool | None = True
    last_updated_at: datetime | None

class RegionSearch(BaseModel):
    data: List[RegionRead]
    pagination: Pagination

class RegionCreate(BaseModel):
    country_id: int
    name: str
    latitude: float
    longitude: float
    osm_id: str
    osm_type: str
    need_automatic_update: bool | None = True

class RegionUpdate(BaseModel):
    region_id: int | None = None
    name: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    osm_id: str | None = None
    osm_type: str | None = None
    need_automatic_update: bool | None = None