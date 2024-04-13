from OSMPythonTools.nominatim import Nominatim


nominatim = Nominatim()

"""
svx = nominatim.query("Кольцово")
print(svx.toJSON())
"""

airports = nominatim.query("SVX")
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

# https://github.com/Loknar/py-iata-lookup

# пиздим парсер сайта ИАТА