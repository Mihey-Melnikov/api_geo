import sys
sys.path.insert(0, 'C:\\Users\\Пользователь\\Desktop\\api_geo')
# todo костыль, нужно разобраться с путями

from src.city.models import city
import asyncio
import csv
from src.osm.NominatimClient import NominatimClient
from src.osm.daemons.utils import try_get_country_id, try_get_region_id, insert_data, CITY_TAGS


async def get_data_from_osm(path: str | None = "C:/Users/Пользователь/Desktop/api_geo/src/osm/daemons/data_to_fill/citys.csv"):
    """
    Get data about city from OSM.
    """
    nc = NominatimClient()
    data = []
    with open(path, encoding='utf8') as r_file:
        rkt_data = csv.DictReader(r_file, delimiter = ",")
        for row in rkt_data:
            city_name = row["name"] if row["name"] != "" else row["latname"]
            print(city_name)
            search_results = nc.search(city_name)
            search_result = {}
            for result in search_results:
                if result["addresstype"] in CITY_TAGS:
                    search_result = result
                    break
            if search_result:
                osm_type = search_result["osm_type"][0]
                osm_id = search_result["osm_id"]
                obj_class = search_result["category"]
                details_result = nc.get_details(osm_type.upper(), osm_id, obj_class)
                country_id = await try_get_country_id(details_result["country_code"])
                if details_result and country_id:
                    region_id = await try_get_region_id(details_result["address"])
                    if str(details_result["osm_id"]) not in [item["osm_id"] for item in data]:
                        new_city = {
                            "name": details_result["names"]["name:ru"] if "name:ru" in details_result["names"] else city_name,
                            "country_id": int(country_id),
                            "region_id": int(region_id) if region_id else None,
                            "timezone": nc.get_timezone(details_result["centroid"]["coordinates"]),
                            "latitude": details_result["centroid"]["coordinates"][1],
                            "longitude": details_result["centroid"]["coordinates"][0],
                            "osm_id": str(details_result["osm_id"]),
                            "osm_type": details_result["osm_type"]
                        }
                        data.append(new_city)
                    else:
                        print(f"Дубликат города: {city_name}")
                else:
                    print(f"Не удалось получить детали города: {city_name}")
            else:
                print(f"Не удалось найти город по запросу: {city_name}")
    return data
            

async def run():
    data = await get_data_from_osm()
    await insert_data(data, city)
