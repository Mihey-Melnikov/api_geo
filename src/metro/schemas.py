from pydantic import BaseModel

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