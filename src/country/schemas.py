from pydantic import BaseModel

class CountryRead(BaseModel):
    id: int
    name: str
    iso3116_alpha2: str
    iso3166_alpha3: str
    phone_code: str
    phone_mask: str
    osm_id: int
    osm_type: str
    need_automatic_update: bool | None = True

class CountryCreate(BaseModel):
    name: str
    iso3116_alpha2: str
    iso3166_alpha3: str
    phone_code: str
    phone_mask: str
    osm_id: int
    osm_type: str
    need_automatic_update: bool | None = True

class CountryUpdate(BaseModel):
    name: str | None = None
    iso3116_alpha2: str | None = None
    iso3166_alpha3: str | None = None
    phone_code: str | None = None
    phone_mask: str | None = None
    osm_id: int | None = None
    osm_type: str | None = None
    need_automatic_update: bool | None = None