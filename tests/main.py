from src.country.router import add_country
from src.region.router import add_region
from src.city.router import add_city
from src.airport.router import add_airport
from src.railway.router import add_railway
from src.metro.router import add_metro
from src.translate.router import add_translate


test_countries = [
    {
        "name": "Россия",
        "iso3116_alpha2": "RU",
        "iso3166_alpha3": "RUS",
        "phone_code": "+7",
        "phone_mask": "(...) ...-..-..",
        "latitude": 64.6863136,
        "longitude": 97.7453061,
        "osm_id": 60189,
        "osm_type": "R",
        "need_automatic_update": True
    }
]

test_regions = [
    {
        "country_id": 1,
        "name": "Свердловская область",
        "latitude": 58.6414755,
        "longitude": 61.8021546,
        "osm_id": 79379,
        "osm_type": "R",
        "need_automatic_update": True
    },
    {
        "country_id": 1,
        "name": "Челябинская область",
        "latitude": 54.4223954,
        "longitude": 61.1865846,
        "osm_id": 77687,
        "osm_type": "R",
        "need_automatic_update": True
    }
]

test_cities = [
    {
        "region_id": 1,
        "country_id": 1,
        "name": "Екатеринбург",
        "iata": "SVX",
        "timezone": "Asia/Yekaterinburg",
        "latitude": 56.839104,
        "longitude": 60.60825,
        "osm_id": 6564910,
        "osm_type": "R",
        "need_automatic_update": True
    },
    {
        "region_id": 2,
        "country_id": 1,
        "name": "Магнитогорск",
        "iata": "MQF",
        "timezone": "Asia/Yekaterinburg",
        "latitude": 53.4242184,
        "longitude": 58.983136,
        "osm_id": 10185071,
        "osm_type": "R",
        "need_automatic_update": True
    }
]

test_airports = [
    {
        "city_id": 1,
        "name": "Кольцово",
        "iata_en": "SXV",
        "iata_ru": "КЛЦ",
        "timezone": "Asia/Yekaterinburg",
        "latitude": 56.74457635,
        "longitude": 60.802790165728474,
        "osm_id": 43102086,
        "osm_type": "W",
        "need_automatic_update": True
    },
    {
        "city_id": 2,
        "name": "Международный аэропорт Магнитогорска",
        "iata_en": "MQF",
        "iata_ru": "МГН",
        "timezone": "Asia/Yekaterinburg",
        "latitude": 53.3938099,
        "longitude": 58.75783291541134,
        "osm_id": 32931637,
        "osm_type": "W",
        "need_automatic_update": True
    }
]

test_railways = [
    {
        "city_id": 1,
        "region_id": 1,
        "country_id": 1,
        "name": "Екатеринбург Пассажирский",
        "express3_code": 2030000,
        "is_main": True,
        "timezone": "Asia/Yekaterinburg",
        "latitude": 56.8595683,
        "longitude": 60.6048898,
        "osm_id": 4795178525,
        "osm_type": "N",
        "need_automatic_update": True
    },
    {
        "city_id": 2,
        "region_id": 2,
        "country_id": 1,
        "name": "Магнитогорск Пассажирский",
        "express3_code": 2040510,
        "is_main": True,
        "timezone": "Asia/Yekaterinburg",
        "latitude": 53.4381623,
        "longitude": 58.9816421,
        "osm_id": 9040047725,
        "osm_type": "N",
        "need_automatic_update": True
    }
]

test_metros = [
    {
        "city_id": 1,
        "station_name": "Геологическая",
        "line_name": "Зеленая",
        "latitude": 56.827831,
        "longitude": 60.6022393,
        "osm_id": 10601241537,
        "osm_type": "N",
        "need_automatic_update": True
    },
    {
        "city_id": 1,
        "station_name": "Площадь 1905 года",
        "line_name": "Зеленая",
        "latitude": 56.8368678,
        "longitude": 60.5991644,
        "osm_id": 10606433480,
        "osm_type": "N",
        "need_automatic_update": True
    }
]

test_translations = [
    {
        "entity": "country",
        "entity_id": 1,
        "translate": [
            {
                "language": "ru",
                "translate": "Россия"
            },
            {
                "language": "en",
                "translate": "Russia"
            },
            {
                "language": "kk",
                "translate": "Ресей"
            }
        ]
    },
    {
        "entity": "region",
        "entity_id": 1,
        "translate": [
            {
                "language": "ru",
                "translate": "Свердловская область"
            },
            {
                "language": "en",
                "translate": "Sverdlovsk region"
            },
            {
                "language": "kk",
                "translate": "Свердлов облысы"
            }
        ]
    },
    {
        "entity": "region",
        "entity_id": 2,
        "translate": [
            {
                "language": "ru",
                "translate": "Челябинская область"
            },
            {
                "language": "en",
                "translate": "Chelyabinsk region"
            },
            {
                "language": "kk",
                "translate": "Челябі облысы"
            }
        ]
    },
    {
        "entity": "city",
        "entity_id": 1,
        "translate": [
            {
                "language": "ru",
                "translate": "Екатеринбург"
            },
            {
                "language": "en",
                "translate": "Ekaterinburg"
            },
            {
                "language": "kk",
                "translate": "Екатеринбург"
            }
        ]
    },
    {
        "entity": "city",
        "entity_id": 2,
        "translate": [
            {
                "language": "ru",
                "translate": "Магнитогорск"
            },
            {
                "language": "en",
                "translate": "Magnitogorsk"
            },
            {
                "language": "kk",
                "translate": "Магнитогорск"
            }
        ]
    },
    {
        "entity": "airport",
        "entity_id": 1,
        "translate": [
            {
                "language": "ru",
                "translate": "Кольцово"
            },
            {
                "language": "en",
                "translate": "Koltsovo"
            },
            {
                "language": "kk",
                "translate": "Сақина"
            }
        ]
    },
    {
        "entity": "airport",
        "entity_id": 2,
        "translate": [
            {
                "language": "ru",
                "translate": "Международный аэропорт Магнитогорск"
            },
            {
                "language": "en",
                "translate": "Magnitogorsk International Airport"
            },
            {
                "language": "kk",
                "translate": "Магнитогорск халықаралық әуежайы"
            }
        ]
    },
    {
        "entity": "railway",
        "entity_id": 1,
        "translate": [
            {
                "language": "ru",
                "translate": "Екатеринбург Пассажирский"
            },
            {
                "language": "en",
                "translate": "Yekaterinburg Passenger"
            },
            {
                "language": "kk",
                "translate": "Екатеринбург Жолаушылар"
            }
        ]
    },
    {
        "entity": "railway",
        "entity_id": 2,
        "translate": [
            {
                "language": "ru",
                "translate": "Магнитогорск Пассажирский"
            },
            {
                "language": "en",
                "translate": "Magnitogorsk Passenger"
            },
            {
                "language": "kk",
                "translate": "Магнитогорск Жолаушылар"
            }
        ]
    },
    {
        "entity": "metro",
        "entity_id": 1,
        "translate": [
            {
                "language": "ru",
                "translate": "Геологическая"
            },
            {
                "language": "en",
                "translate": "Geologicheskaya"
            },
            {
                "language": "kk",
                "translate": "Геологическая"
            }
        ]
    },
    {
        "entity": "metro",
        "entity_id": 2,
        "translate": [
            {
                "language": "ru",
                "translate": "Площадь 1905 года"
            },
            {
                "language": "en",
                "translate": "Ploshad 1905 goda"
            },
            {
                "language": "kk",
                "translate": "Площадь 1905 года"
            }
        ]
    },
]

