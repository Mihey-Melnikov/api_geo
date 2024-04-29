import sys
sys.path.insert(0, 'C:\\Users\\Пользователь\\Desktop\\api_geo')
# todo костыль, нужно разобраться с путями

from src.country.models import country
import asyncio
import csv
from src.osm.NominatimClient import NominatimClient
from src.osm.daemons.utils import insert_data


def get_data_from_osm():
    nc = NominatimClient()
    data = []
    with open("C:/Users/Пользователь/Desktop/api_geo/src/osm/daemons/data_to_fill/countrys.csv", encoding='utf8') as r_file:
        start_data = csv.DictReader(r_file, delimiter = ",")        
        for row in start_data:
            search_results = nc.search(row["name"]) 
            search_result = {}
            for result in search_results:
                if result["addresstype"] == "country":
                    search_result = result
                    break
            if search_result:
                osm_type = search_result["osm_type"][0]
                osm_id = search_result["osm_id"]
                obj_class = search_result["category"]
                details_result = nc.get_details(osm_type.upper(), osm_id, obj_class)
                if details_result:
                    new_country = {
                        "name": details_result["names"]["name:ru"] if "name:ru" in details_result["names"] else row["name"],
                        "iso3116_alpha2": details_result["extratags"]["ISO3166-1:alpha2"] if "ISO3166-1:alpha2" in details_result["extratags"] else row["iso3_alpha2"],
                        "iso3166_alpha3": details_result["extratags"]["ISO3166-1:alpha3"] if "ISO3166-1:alpha3" in details_result["extratags"] else row["iso3_alpha3"],
                        "phone_code": row["phone_code"] if row["phone_code"] is not None and row["phone_code"] != "" and row["phone_code"] != "NULL" else None,
                        "phone_mask": row["phone_mask"] if row["phone_mask"] is not None and row["phone_mask"] != "" and row["phone_mask"] != "NULL" else None,
                        "latitude": details_result["centroid"]["coordinates"][0],
                        "longitude": details_result["centroid"]["coordinates"][1],
                        "osm_id": str(details_result["osm_id"]),
                        "osm_type": details_result["osm_type"],
                    }
                    data.append(new_country)
                else:
                    print(f"Не удалось получить детали страны: {row['name']}")
            else:
                print(f"Не удалось найти страну по запросу: {row['name']}")
    return data
            

async def main():
    data = get_data_from_osm()
    await insert_data(data, country)

# todo переделать в формат скрипта с параметрами запуска
asyncio.run(main())