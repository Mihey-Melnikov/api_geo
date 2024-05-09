import sys
sys.path.insert(0, 'C:\\Users\\Пользователь\\Desktop\\api_geo')
# todo костыль, нужно разобраться с путями

from src.railway.models import railway
import asyncio
import csv
import re
from src.osm.NominatimClient import NominatimClient
from src.osm.daemons.utils import insert_data, RAILWAY_TAGS, try_get_city_id, try_get_express_by_osm, update_data, try_get_country_id, try_get_region_id


async def get_data_from_osm(path: str | None = "C:/Users/Пользователь/Desktop/api_geo/src/osm/daemons/data_to_fill/rzd_railway_station.csv"):
    nc = NominatimClient()
    railway_data = []
    city_ids = []
    with open(path, encoding='utf8') as r_file:
        rkt_data = csv.DictReader(r_file, delimiter = ",") 
        for row in rkt_data:
            try:
                railway_name = row["full_name_ru"] if row["full_name_ru"] != "" else row["full_name_en"]
                print(railway_name)
                if row["osm_type"] and row["osm_id"]:
                    osm_type = row["osm_type"]
                    osm_id = row["osm_id"]
                    obj_class = "railway"
                    # print(osm_type, osm_id, obj_class)
                    details_result = nc.get_details(osm_type.upper(), osm_id, obj_class)
                    # print(details_result)
                    city_id = await try_get_city_id(details_result["address"], details_result["centroid"]["coordinates"])
                    region_id = await try_get_region_id(details_result["address"])
                    country_id = await try_get_country_id(details_result["country_code"])
                    if details_result and city_id:
                        express3 = await try_get_express_by_osm(str(osm_id))
                        if str(details_result["osm_id"]) not in [item["osm_id"] for item in railway_data]:
                            name = details_result["names"]["name:ru"] if "name:ru" in details_result["names"] else railway_name
                            if city_id not in city_ids:
                                is_main = True
                                city_ids.append(city_id)
                            else:
                                is_main = False
                            new_railway = {
                                "name": name,
                                "express3_code": str(express3),
                                "is_main": is_main,
                                "city_id": int(city_id) if city_id else None,
                                "region_id": int(region_id) if region_id else None,
                                "country_id": int(country_id),
                                "timezone": nc.get_timezone(details_result["centroid"]["coordinates"]),
                                "latitude": details_result["centroid"]["coordinates"][1],
                                "longitude": details_result["centroid"]["coordinates"][0],
                                "osm_id": str(details_result["osm_id"]),
                                "osm_type": details_result["osm_type"],
                            }
                            railway_data.append(new_railway)
                        else:
                            print(f"Дубликат ЖД станции: {railway_name}")
                    else:
                        print(f"Не удалось получить детали ЖД станции: {railway_name}")
                else:
                    print(f"Не удалось найти ЖД станцию по запросу: {railway_name}")
            except KeyboardInterrupt:
                assert KeyboardInterrupt
                break
            except:
                print(f"Произошла ошибка")
    return railway_data


async def run(path):
    railway_data = await get_data_from_osm(path)
    await insert_data(railway_data, railway)