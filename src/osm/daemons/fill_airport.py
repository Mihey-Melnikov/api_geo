import sys
sys.path.insert(0, 'C:\\Users\\Пользователь\\Desktop\\api_geo')
# todo костыль, нужно разобраться с путями

from src.airport.models import airport
from src.city.models import city
import asyncio
import csv
import re
from src.osm.NominatimClient import NominatimClient
from src.osm.daemons.utils import insert_data, AIRPORT_TAGS, try_get_city_id, update_data


async def get_data_from_osm():
    nc = NominatimClient()
    airport_data = []
    city_data = []
    with open("C:/Users/Пользователь/Desktop/api_geo/src/osm/daemons/data_to_fill/airports.csv", encoding='utf8') as r_file:
        rkt_data = csv.DictReader(r_file, delimiter = ",")        
        for row in rkt_data:
            try:
                airport_name = row["name_en"]
                print(airport_name)
                search_results = nc.search(airport_name) + nc.search(row["code_en"])
                search_result = {}
                for result in search_results:
                    if result["addresstype"] in AIRPORT_TAGS:
                        search_result = result
                        break
                if search_result:
                    osm_type = search_result["osm_type"][0]
                    osm_id = search_result["osm_id"]
                    obj_class = search_result["category"]
                    details_result = nc.get_details(osm_type.upper(), osm_id, obj_class)
                    city_id = await try_get_city_id(details_result["address"], details_result["centroid"]["coordinates"])
                    if details_result and city_id:
                        iata = details_result["names"]["iata"] if "iata" in details_result["names"] and len(details_result["names"]["iata"]) == 3 else details_result["names"]["ref"] if "ref" in details_result["names"] and len(details_result["names"]["ref"]) == 3 else row["code_en"]
                        if str(details_result["osm_id"]) not in [item["osm_id"] for item in airport_data]:
                            name = ''
                            if "name:ru" in details_result["names"]:
                                if search_result["addresstype"] == "railway":
                                    name = f"Стойка регистрации {details_result['names']['name:ru']}"
                                else:
                                    name = details_result["names"]["name:ru"]
                            else:
                                name = airport_name
                            new_airport = {
                                "name": name,
                                "city_id": int(city_id),
                                "iata_en": None if bool(re.search('[а-яА-Я]', iata)) else iata,
                                "iata_ru": iata if bool(re.search('[а-яА-Я]', iata)) else None,
                                "timezone": nc.get_timezone(details_result["centroid"]["coordinates"]),
                                "latitude": details_result["centroid"]["coordinates"][1],
                                "longitude": details_result["centroid"]["coordinates"][0],
                                "osm_id": str(details_result["osm_id"]),
                                "osm_type": details_result["osm_type"],
                            }
                            city_iata = {
                                "id": city_id,
                                "iata": iata,
                            }
                            airport_data.append(new_airport)
                            city_data.append(city_iata)
                        else:
                            print(f"Дубликат аэропорта: {airport_name}")
                    else:
                        print(f"Не удалось получить детали аэропорта: {airport_name}")
                else:
                    print(f"Не удалось найти аэропорт по запросу: {airport_name}")
            except:
                print("Что-то упало...")
    return airport_data, city_data


async def fill_city_iata_by_airport():
    pass

async def main():
    airport_data, city_data = await get_data_from_osm()
    await insert_data(airport_data, airport)
    await update_data(city_data, city)

# todo переделать в формат скрипта с параметрами запуска
asyncio.run(main())



"""
Tags
aeroway=aerodrome
aeroway=heliport
aeroway=runway
aeroway=taxiway
aeroway=apron
aeroway=terminal
aeroway=helipad
aeroway=spaceport
aeroway=airstrip
"""
