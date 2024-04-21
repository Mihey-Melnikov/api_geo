from datetime import datetime
from typing import List
from pydantic import BaseModel, Field

class Pagination(BaseModel):
    page_number: int = Field(..., description="The current page number", example=1)
    page_size: int = Field(..., description="The number of items per page", example=100)
    total_pages: int = Field(..., description="The total number of pages available", example=5)

class AirportRead(BaseModel):
    id: int = Field(..., description="The unique identifier for the airport", example=1)
    city_id: int = Field(..., description="The identifier for the city where the airport is located", example=1)
    name: str = Field(..., description="The name of the airport", example="Кольцово")
    iata_en: str | None = Field(None, description="The international IATA code in English", example="SXV")
    iata_ru: str | None = Field(None, description="The international IATA code in Russian", example="КЛЦ")
    timezone: str = Field(..., description="The timezone of the airport by IANA format", example="Asia/Yekaterinburg")
    latitude: float = Field(..., description="The latitude coordinate of the airport", example=56.74457635)
    longitude: float = Field(..., description="The longitude coordinate of the airport", example=60.802790165728474)
    osm_id: int = Field(..., description="The OpenStreetMap identifier for the airport", example=43102086)
    osm_type: str = Field(..., description="The OpenStreetMap type for the airport", example="W")
    need_automatic_update: bool | None = Field(True, description="Flag indicating if automatic updates are needed", example=True)
    last_updated_at: datetime = Field(..., description="The timestamp of the last update", example=datetime.now())
    deleted_at: datetime | None =  Field(None, description="The timestamp of when the airport was deleted", example=datetime.now())

class AirportSearch(BaseModel):
    data: List[AirportRead] = Field(..., description="A list of airports matching the search criteria")
    pagination: Pagination = Field(..., description="Pagination details for the search results")

class AirportCreate(BaseModel):
    city_id: int = Field(..., description="The identifier for the city where the airport is located", example=1)
    name: str = Field(..., description="The name of the airport", example="Кольцово")
    iata_en: str | None = Field(None, description="The international IATA code in English", example="SXV")
    iata_ru: str | None = Field(None, description="The international IATA code in Russian", example="КЛЦ")
    timezone: str = Field(..., description="The timezone of the airport by IANA format", example="Asia/Yekaterinburg")
    latitude: float = Field(..., description="The latitude coordinate of the airport", example=56.74457635)
    longitude: float = Field(..., description="The longitude coordinate of the airport", example=60.802790165728474)
    osm_id: int = Field(..., description="The OpenStreetMap identifier for the airport", example=43102086)
    osm_type: str = Field(..., description="The OpenStreetMap type for the airport", example="W")
    need_automatic_update: bool | None = Field(True, description="Flag indicating if automatic updates are needed", example=True)

class AirportUpdate(BaseModel):
    city_id: int | None = Field(None, description="The identifier for the city where the airport is located", example=1)
    name: str | None = Field(None, description="The name of the airport", example="Кольцово")
    iata_en: str | None = Field(None, description="The international IATA code in English", example="SXV")
    iata_ru: str | None = Field(None, description="The international IATA code in Russian", example="КЛЦ")
    timezone: str | None = Field(None, description="The timezone of the airport by IANA format", example="Asia/Yekaterinburg")
    latitude: float | None = Field(None, description="The latitude coordinate of the airport", example=56.74457635)
    longitude: float | None = Field(None, description="The longitude coordinate of the airport", example=60.802790165728474)
    osm_id: int | None = Field(None, description="The OpenStreetMap identifier for the airport", example=43102086)
    osm_type: str | None = Field(None, description="The OpenStreetMap type for the airport", example="W")
    need_automatic_update: bool | None = Field(None, description="Flag indicating if automatic updates are needed", example=True)
    deleted_at: datetime | None =  Field(None, description="The timestamp of when the airport was deleted")
