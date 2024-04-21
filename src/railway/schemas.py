from datetime import datetime
from typing import List
from pydantic import BaseModel

class Pagination(BaseModel):
    page_number: int
    page_size: int
    total_pages: int

class RailwayRead(BaseModel):
    id: int
    city_id: int | None = None
    region_id: int | None = None
    country_id: int
    name: str
    express3_code: str
    is_main: bool
    timezone: str
    latitude: float
    longitude: float
    osm_id: int
    osm_type: str
    need_automatic_update: bool | None = True
    last_updated_at: datetime
    deleted_at: datetime | None

class RailwaySearch(BaseModel):
    data: List[RailwayRead]
    pagination: Pagination

class RailwayCreate(BaseModel):
    city_id: int | None = None
    region_id: int | None = None
    country_id: int
    name: str
    express3_code: int
    is_main: bool
    timezone: str
    latitude: float
    longitude: float
    osm_id: int
    osm_type: str
    need_automatic_update: bool | None = True

class RailwayUpdate(BaseModel):
    city_id: int | None = None
    region_id: int | None = None
    country_id: int | None = None
    name: str | None = None
    express3_code: int | None = None
    is_main: bool | None = None
    timezone: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    osm_id: int | None = None
    osm_type: str | None = None
    need_automatic_update: bool | None = None
    deleted_at: datetime | None = None