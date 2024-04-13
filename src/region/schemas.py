from pydantic import BaseModel

class RegionRead(BaseModel):
    id: int
    country_id: int
    name: str
    osm_id: int
    osm_type: str
    need_automatic_update: bool | None = True

class RegionCreate(BaseModel):
    country_id: int
    name: str
    osm_id: int
    osm_type: str
    need_automatic_update: bool | None = True

class RegionUpdate(BaseModel):
    region_id: int | None = None
    name: str | None = None
    osm_id: int | None = None
    osm_type: str | None = None
    need_automatic_update: bool | None = None