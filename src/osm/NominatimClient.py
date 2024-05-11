import requests
from timezonefinder import TimezoneFinder

class NominatimClient:
    def __init__(self):
        self.base_url = "https://nominatim.openstreetmap.org"
        self.tz = TimezoneFinder()

    def search(self, query):
        endpoint = "/search"
        params = {
            "q": query,
            "polygon_geojson": 1,
            "format": "jsonv2"
        }
        response = requests.get(self.base_url + endpoint, params=params)
        return response.json() if response.status_code != 403 else []

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
        return response.json() if response.status_code != 403 else []
    
    def get_timezone(self, coordinates):
        return self.tz.timezone_at(lng=coordinates[0], lat=coordinates[1])
