import sys
sys.path.insert(0, 'C:\\Users\\Пользователь\\Desktop\\api_geo')
# todo костыль, нужно разобраться с путями

from src.region.models import region
import asyncio
import csv
from src.osm.NominatimClient import NominatimClient
from src.osm.daemons.utils import REGION_TAGS, try_get_country_id, insert_data


async def get_data_from_osm(path: str | None = "C:/Users/Пользователь/Desktop/api_geo/src/osm/daemons/data_to_fill/brn_city_region.csv"):
    """
    Get data about region from OSM.
    """
    nc = NominatimClient()
    data = []
    with open(path, encoding='utf8') as r_file:
        rkt_data = csv.DictReader(r_file, delimiter = ",")        
        for row in rkt_data:
            region_name = row["name"] if row["name"] != "" else row["name_en"]
            print(region_name)
            search_results = nc.search(region_name)
            search_result = {}
            for result in search_results:
                if result["addresstype"] in REGION_TAGS:
                    search_result = result
                    break
            if search_result:
                osm_type = search_result["osm_type"][0]
                osm_id = search_result["osm_id"]
                obj_class = search_result["category"]
                details_result = nc.get_details(osm_type.upper(), osm_id, obj_class)
                country_id = await try_get_country_id(details_result["country_code"])
                if details_result and country_id:
                    if str(details_result["osm_id"]) not in [item["osm_id"] for item in data]:
                        new_region = {
                            "name": details_result["names"]["name:ru"] if "name:ru" in details_result["names"] else region_name,
                            "country_id": int(country_id),
                            "latitude": details_result["centroid"]["coordinates"][1],
                            "longitude": details_result["centroid"]["coordinates"][0],
                            "osm_id": str(details_result["osm_id"]),
                            "osm_type": details_result["osm_type"]
                        }
                        data.append(new_region)
                    else:
                        print(f"Дубликат региона: {region_name}")
                else:
                    print(f"Не удалось получить детали региона: {region_name}")
            else:
                print(f"Не удалось найти регион по запросу: {region_name}")
    return data
            

async def run(path):
    data = await get_data_from_osm(path)
    await insert_data(data, region)
