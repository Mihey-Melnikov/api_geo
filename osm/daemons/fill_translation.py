import sys
sys.path.insert(0, 'C:\\Users\\Пользователь\\Desktop\\api_geo')
# todo костыль, нужно разобраться с путями

from requests import HTTPError, ConnectionError
from src.translate.models import translate, language
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import engine
from osm.daemons.utils import insert_data
from sqlalchemy import select, Table
from src.country.models import country
from src.region.models import region
from src.city.models import city
from src.airport.models import airport
from src.railway.models import railway
import translators as ts
from logger.logger import get_script_logger


logger = get_script_logger("translate")


async def get_translations(entity: str, entity_model: Table):
    data = []
    async with AsyncSession(engine) as session:
        async with session.begin():
            result = await session.execute(select(entity_model))
        objs = result.mappings().all()

        async with session.begin():
            result = await session.execute(select(language.c.language_iso639))
        langs = [item["language_iso639"] for item in result.mappings().all()]

        for obj in objs:
            logger.info(f"Add: {obj['name']}")
            for lang in langs:
                try:
                    transl = ts.translate_text(obj["name"], to_language=lang)
                    data.append({
                        "entity": entity,
                        "entity_id": obj["id"],
                        "language": lang,
                        "translate": transl
                    })
                except HTTPError:
                    logger.error(f"An error {HTTPError} dropped on the word {obj['name']}")
                except ConnectionError:
                    logger.error(f"An error {ConnectionError} dropped on the word {obj['name']}")
                except:
                    logger.critical(f"The translate script has crashed")
    return data


async def run():
    for entity, entity_model in [
            ("country", country), 
            ("region", region), 
            ("city", city), 
            ("airport", airport), 
            ("railway", railway)]:
        logger.info(f"================== Start Translate[{entity}] Fill Script ==================")
        data = await get_translations(entity, entity_model)
        await insert_data(data, translate)
        logger.info(f"================== End Translate[{entity}] Fill Script ==================")
    
