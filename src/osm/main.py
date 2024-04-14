from OSMPythonTools.nominatim import Nominatim
from OSMPythonTools.api import Api, ApiResult
from timezonefinder import TimezoneFinder

tf = TimezoneFinder()  # reuse

query_points = [(56.78814745, 60.61984225300779)]
for lng, lat in query_points:
    tz = tf.timezone_at(lng=lng, lat=lat)  # 'Europe/Berlin'

print(tz)

api = Api()
way = api.query("way/43102086")
print(way.tags())
print()

nominatim = Nominatim()

"""
svx = nominatim.query("Кольцово")
print(svx.toJSON())
"""

airports = nominatim.query("городской округ Екатеринбург")
print(airports.toJSON())

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

# https://pypi.org/project/airports-py/

# https://github.com/Loknar /py-iata-lookup

# пиздим парсер сайта ИАТА