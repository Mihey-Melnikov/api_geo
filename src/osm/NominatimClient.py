import requests

class NominatimClient:
    def __init__(self):
        self.base_url = "https://nominatim.openstreetmap.org"

    def search(self, query):
        endpoint = "/search"
        params = {
            "q": query,
            "polygon_geojson": 1,
            "format": "jsonv2"
        }
        response = requests.get(self.base_url + endpoint, params=params)
        return response.json()

    def get_details(self, osm_type, osm_id, obj_class):
        endpoint = "/details"
        params = {
            "osmtype": osm_type,
            "osmid": osm_id,
            "class": obj_class,
            "addressdetails": 1,
            "hierarchy": 0,
            "group_hierarchy": 1,
            "polygon_geojson": 1,
            "format": "json"
        }
        response = requests.get(self.base_url + endpoint, params=params)
        return response.json()

# Пример использования:
nominatim_client = NominatimClient()
search_result = nominatim_client.search("Кольцово")
print(search_result)
if search_result:
    first_place_id = search_result[0]["place_id"]
    details_result = nominatim_client.get_details("W", 43102086, "aeroway")
    if details_result:
        print(f"Детали места (place_id={first_place_id}):")
        print(details_result)
    else:
        print("Не удалось получить детали места.")
else:
    print("Не удалось найти место по запросу.")