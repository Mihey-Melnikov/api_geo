from httpx import AsyncClient
import pytest

@pytest.mark.order(1)
async def test_add_country(ac: AsyncClient):
    response = await ac.post("/api/country/", json={
        "name": "Россия",
        "iso3116_alpha2": "RU",
        "iso3166_alpha3": "RUS",
        "phone_code": "+7",
        "phone_mask": "(...) ...-..-..",
        "latitude": 64.6863136,
        "longitude": 97.7453061,
        "osm_id": "60189",
        "osm_type": "R",
        "need_automatic_update": True
    })

    assert response.status_code == 200

@pytest.mark.order(2)
async def test_add_translate_for_country(ac: AsyncClient):
    response1 = await ac.post("/api/translate/", json=[
        {
            "entity": "country",
            "entity_id": 1,
            "language": "ru",
            "translate": "Россия"
        },
        {
            "entity": "country",
            "entity_id": 1,
            "language": "en",
            "translate": "Russia"
        },
        {
            "entity": "country",
            "entity_id": 1,
            "language": "kk",
            "translate": "Россия"
        }
    ])
    assert response1.status_code == 200

async def test_get_country_by_id(ac: AsyncClient):
    response = await ac.get("/api/country/", params={
        "id": 1,
    })

    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["name"] == "Россия"

@pytest.mark.order(3)
async def test_add_region(ac: AsyncClient):
    response1 = await ac.post("/api/region/", json={
        "country_id": 1,
        "name": "Свердловская область",
        "latitude": 58.6414755,
        "longitude": 61.8021546,
        "osm_id": "79379",
        "osm_type": "R",
        "need_automatic_update": True
    })
    assert response1.status_code == 200

    response2 = await ac.post("/api/region/", json={
        "country_id": 1,
        "name": "Челябинская область",
        "latitude": 54.4223954,
        "longitude": 61.1865846,
        "osm_id": "77687",
        "osm_type": "R",
        "need_automatic_update": True
    })
    assert response2.status_code == 200

@pytest.mark.order(4)
async def test_add_translate_for_region(ac: AsyncClient):
    response1 = await ac.post("/api/translate/", json=[
        {
            "entity": "region",
            "entity_id": 1,
            "language": "ru",
            "translate": "Свердловская область"
        },
        {
            "entity": "region",
            "entity_id": 1,
            "language": "en",
            "translate": "Sverdlovsk region"
        },
        {
            "entity": "region",
            "entity_id": 1,
            "language": "kk",
            "translate": "Свердловская область"
        }
    ])
    assert response1.status_code == 200

    response1 = await ac.post("/api/translate/", json=[
        {
            "entity": "region",
            "entity_id": 2,
            "language": "ru",
            "translate": "Челябинская область"
        },
        {
            "entity": "region",
            "entity_id": 2,
            "language": "en",
            "translate": "Chelyabinsk region"
        },
        {
            "entity": "region",
            "entity_id": 2,
            "language": "kk",
            "translate": "Челябинская область"
        }
    ])
    assert response1.status_code == 200

@pytest.mark.order(5)
async def test_add_city(ac: AsyncClient):
    response1 = await ac.post("/api/city/", json={
        "region_id": 1,
        "country_id": 1,
        "name": "Екатеринбург",
        "iata": "SVX",
        "timezone": "Asia/Yekaterinburg",
        "latitude": 56.839104,
        "longitude": 60.60825,
        "osm_id": "6564910",
        "osm_type": "R",
        "need_automatic_update": True
    })
    assert response1.status_code == 200

    response2 = await ac.post("/api/city/", json={
        "region_id": 2,
        "country_id": 1,
        "name": "Магнитогорск",
        "iata": "MQF",
        "timezone": "Asia/Yekaterinburg",
        "latitude": 53.4242184,
        "longitude": 58.983136,
        "osm_id": "10185071",
        "osm_type": "R",
        "need_automatic_update": True
    })
    assert response2.status_code == 200

@pytest.mark.order(6)
async def test_add_translate_for_city(ac: AsyncClient):
    response1 = await ac.post("/api/translate/", json=[
        {
            "entity": "city",
            "entity_id": 1,
            "language": "ru",
            "translate": "Екатеринбург"
        },
        {
            "entity": "city",
            "entity_id": 1,
            "language": "en",
            "translate": "Ekaterinburg"
        },
        {
            "entity": "city",
            "entity_id": 1,
            "language": "kk",
            "translate": "Екатеринбург"
        }
    ])
    assert response1.status_code == 200

    response1 = await ac.post("/api/translate/", json=[
        {
            "entity": "city",
            "entity_id": 2,
            "language": "ru",
            "translate": "Магнитогорск"
        },
        {
            "entity": "city",
            "entity_id": 2,
            "language": "en",
            "translate": "Magnitogorsk"
        },
        {
            "entity": "city",
            "entity_id": 2,
            "language": "kk",
            "translate": "Магнитогорск"
        }
    ])
    assert response1.status_code == 200

@pytest.mark.order(7)
async def test_add_airport(ac: AsyncClient):
    response1 = await ac.post("/api/airport/", json={
        "city_id": 1,
        "name": "Кольцово",
        "iata_en": "SXV",
        "iata_ru": "КЛЦ",
        "timezone": "Asia/Yekaterinburg",
        "latitude": 56.74457635,
        "longitude": 60.802790165728474,
        "osm_id": "43102086",
        "osm_type": "W",
        "need_automatic_update": True
    })
    assert response1.status_code == 200

    response2 = await ac.post("/api/airport/", json={
        "city_id": 2,
        "name": "Международный аэропорт Магнитогорска",
        "iata_en": "MQF",
        "iata_ru": "МГН",
        "timezone": "Asia/Yekaterinburg",
        "latitude": 53.3938099,
        "longitude": 58.75783291541134,
        "osm_id": "32931637",
        "osm_type": "W",
        "need_automatic_update": True
    })
    assert response2.status_code == 200

@pytest.mark.order(8)
async def test_add_translate_for_airport(ac: AsyncClient):
    response1 = await ac.post("/api/translate/", json=[
        {
            "entity": "airport",
            "entity_id": 1,
            "language": "ru",
            "translate": "Кольцово"
        },
        {
            "entity": "airport",
            "entity_id": 1,
            "language": "en",
            "translate": "Koltsovo"
        },
        {
            "entity": "airport",
            "entity_id": 1,
            "language": "kk",
            "translate": "Кольцово"
        }
    ])
    assert response1.status_code == 200

    response1 = await ac.post("/api/translate/", json=[
        {
            "entity": "airport",
            "entity_id": 2,
            "language": "ru",
            "translate": "Международный аэропорт Магнитогорск"
        },
        {
            "entity": "airport",
            "entity_id": 2,
            "language": "en",
            "translate": "Magnitogorsk International Airport"
        },
        {
            "entity": "airport",
            "entity_id": 2,
            "language": "kk",
            "translate": "Международный аэропорт Магнитогорск"
        }
    ])
    assert response1.status_code == 200

@pytest.mark.order(9)
async def test_add_railway(ac: AsyncClient):
    response1 = await ac.post("/api/railway/", json={
        "city_id": 1,
        "region_id": 1,
        "country_id": 1,
        "name": "Екатеринбург Пассажирский",
        "express3_code": "2030000",
        "is_main": True,
        "timezone": "Asia/Yekaterinburg",
        "latitude": 56.8595683,
        "longitude": 60.6048898,
        "osm_id": "4795178525",
        "osm_type": "N",
        "need_automatic_update": True
    })
    assert response1.status_code == 200

    response2 = await ac.post("/api/railway/", json={
        "city_id": 2,
        "region_id": 2,
        "country_id": 1,
        "name": "Магнитогорск Пассажирский",
        "express3_code": "2040510",
        "is_main": True,
        "timezone": "Asia/Yekaterinburg",
        "latitude": 53.4381623,
        "longitude": 58.9816421,
        "osm_id": "9040047725",
        "osm_type": "N",
        "need_automatic_update": True
    })
    assert response2.status_code == 200

@pytest.mark.order(10)
async def test_add_translate_for_railway(ac: AsyncClient):
    response1 = await ac.post("/api/translate/", json=[
        {
            "entity": "railway",
            "entity_id": 1,
            "language": "ru",
            "translate": "Екатеринбург Пассажирский"
        },
        {
            "entity": "railway",
            "entity_id": 1,
            "language": "en",
            "translate": "Yekaterinburg Passenger"
        },
        {
            "entity": "railway",
            "entity_id": 1,
            "language": "kk",
            "translate": "Екатеринбург Пассажирский"
        }
    ])
    assert response1.status_code == 200

    response1 = await ac.post("/api/translate/", json=[
        {
            "entity": "railway",
            "entity_id": 2,
            "language": "ru",
            "translate": "Магнитогорск Пассажирский"
        },
        {
            "entity": "railway",
            "entity_id": 2,
            "language": "en",
            "translate": "Magnitogorsk Passenger"
        },
        {
            "entity": "railway",
            "entity_id": 2,
            "language": "kk",
            "translate": "Магнитогорск Пассажирский"
        }
    ])
    assert response1.status_code == 200

@pytest.mark.order(11)
async def test_add_metro(ac: AsyncClient):
    response1 = await ac.post("/api/metro/", json={
        "city_id": 1,
        "station_name": "Геологическая",
        "line_name": "Зеленая",
        "latitude": 56.827831,
        "longitude": 60.6022393,
        "osm_id": "10601241537",
        "osm_type": "N",
        "need_automatic_update": True
    })
    assert response1.status_code == 200

    response2 = await ac.post("/api/metro/", json={
        "city_id": 1,
        "station_name": "Площадь 1905 года",
        "line_name": "Зеленая",
        "latitude": 56.8368678,
        "longitude": 60.5991644,
        "osm_id": "10606433480",
        "osm_type": "N",
        "need_automatic_update": True
    })
    assert response2.status_code == 200

@pytest.mark.order(12)
async def test_add_translate_for_metro(ac: AsyncClient):
    response1 = await ac.post("/api/translate/", json=[
        {
            "entity": "metro",
            "entity_id": 1,
            "language": "ru",
            "translate": "Геологическая"
        },
        {
            "entity": "metro",
            "entity_id": 1,
            "language": "en",
            "translate": "Geologicheskaya"
        },
        {
            "entity": "metro",
            "entity_id": 1,
            "language": "kk",
            "translate": "Геологическая"
        }
    ])
    assert response1.status_code == 200

    response1 = await ac.post("/api/translate/", json=[
        {
            "entity": "metro",
            "entity_id": 2,
            "language": "ru",
            "translate": "Площадь 1905 года"
        },
        {
            "entity": "metro",
            "entity_id": 2,
            "language": "en",
            "translate": "Ploshad 1905 goda"
        },
        {
            "entity": "metro",
            "entity_id": 2,
            "language": "kk",
            "translate": "Площадь 1905 года"
        }
    ])
    assert response1.status_code == 200
