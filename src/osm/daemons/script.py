import asyncio
import sys
sys.path.insert(0, 'C:\\Users\\Пользователь\\Desktop\\api_geo')
# todo костыль, нужно разобраться с путями

import argparse
from src.country.models import country
from src.region.models import region
from src.city.models import city
from src.airport.models import airport
from src.railway.models import railway
from src.translate.models import translation
import src.osm.daemons.fill_country as fill_country
import src.osm.daemons.fill_region as fill_region
import src.osm.daemons.fill_city as fill_city
import src.osm.daemons.fill_airport as fill_airport
import src.osm.daemons.fill_railway as fill_railway
import src.osm.daemons.fill_translation as fill_translation
from src.osm.daemons.utils import update_table, table_is_empty


MODELS = {
    "country": country,
    "region": region,
    "city": city,
    "airport": airport,
    "railway": railway,
    "translation": translation,
    "all": [country, region, city, airport, railway, translation]
}

PARSER = argparse.ArgumentParser(description="A script for filling in and updating geographical data")
PARSER.add_argument(
    "--action", "-a",
    required=True,
    type=str,
    help="Script action: filling in data or updating",
    choices=["fill", "update"]
)
PARSER.add_argument(
    "--entity", "-e",
    required=True,
    type=str,
    help="The type of geographical object to apply the script to",
    choices=["country", "region", "city", "airport", "railway", "translate", "all"]
)
PARSER.add_argument(
    "--ids", "-i",
    required=False,
    type=str,
    default=None,
    help="ID of the objects to update"
)
PARSER.add_argument(
    "--loging", "-l",
    required=False,
    default=False,
    type=bool,
    help="The need to log the script launch"
)
PARSER.add_argument(
    "--logpath", "-lp",
    required=False,
    default="./logs",
    type=str,
    help="The path to the folder for saving logs"
)
PARSER.add_argument(
    "--datapath", "-dp",
    required=False,
    type=str,
    help="Path to file with start data to fill table"
)


async def main():
    args = PARSER.parse_args()

    if args.action == "fill":
        if not table_is_empty(MODELS[args.entity]):
            print(f"Table {MODELS[args.entity]} is not empty. First you need to clear the table.")
            exit
        else:
            if args.entity == "country":
                await fill_country.run(args.datapath)
            elif args.entity == "region":
                await fill_region.run(args.datapath)
            elif args.entity == "city":
                await fill_city.run(args.datapath)
            elif args.entity == "airport":
                await fill_airport.run(args.datapath)
            elif args.entity == "railway":
                await fill_railway.run(args.datapath)
            elif args.entity == "translate":
                await fill_translation.run()
            elif args.entity == "all":
                await fill_country.run(args.datapath)
                await fill_region.run(args.datapath)
                await fill_city.run(args.datapath)
                await fill_airport.run(args.datapath)
                await fill_railway.run(args.datapath)
                await fill_translation.run()
            else:
                assert Exception("Fatal Exception")

    if args.action == 'update':
        await update_table(MODELS['args.entity'])


asyncio.run(main())
