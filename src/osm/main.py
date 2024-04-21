from OSMPythonTools.nominatim import Nominatim, NominatimResult
from OSMPythonTools.api import Api, ApiResult
from timezonefinder import TimezoneFinder

tf = TimezoneFinder()  # reuse

query_points = [(56.78814745, 60.61984225300779)]
for lng, lat in query_points:
    tz = tf.timezone_at(lng=lng, lat=lat)  # 'Europe/Berlin'


"""print(tz)

api = Api()
way = api.query("way/75208070")
print(way.tags())
print()
print(way.address())

input()"""

nominatim = Nominatim(endpoint='https://nominatim.openstreetmap.org/details')

"""
svx = nominatim.query("Кольцово")
print(svx.toJSON())
"""

airports = nominatim.query("osmtype=W&osmid=43102086&class=aeroway")
print(airports.address())
print()

input()




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

для поиска нужен запрос https://nominatim.openstreetmap.org/search
для деталей https://nominatim.openstreetmap.org/details

"""

# https://pypi.org/project/airports-py/

# https://github.com/Loknar /py-iata-lookup

# пиздим парсер сайта ИАТА