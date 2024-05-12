from fastapi import FastAPI
from src.auth.base_config import auth_backend, fastapi_users
from src.auth.schemas import UserRead, UserCreate
from src.city.router import router as router_city
from src.region.router import router as router_region
from src.country.router import router as router_country
from src.airport.router import router as router_airport
from src.railway.router import router as router_railway
# from src.metro.router import router as router_metro
from src.translate.router import router as router_translate

app = FastAPI(
    title="API Geo"
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_users_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(router_country)
app.include_router(router_region)
app.include_router(router_city)
app.include_router(router_airport)
app.include_router(router_railway)
# app.include_router(router_metro)
app.include_router(router_translate)