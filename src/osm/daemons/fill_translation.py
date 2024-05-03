import sys
sys.path.insert(0, 'C:\\Users\\Пользователь\\Desktop\\api_geo')
# todo костыль, нужно разобраться с путями

from requests import HTTPError
from src.translate.models import translation, translation_language
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
from src.database import engine
from src.osm.daemons.utils import insert_data
from sqlalchemy import select, Table
from src.country.models import country
from src.region.models import region
import translators as ts


async def get_translations(entity: str, entity_model: Table):
    data = []
    async with AsyncSession(engine) as session:
        async with session.begin():
            result = await session.execute(select(entity_model))
        objs = result.mappings().all()

        async with session.begin():
            result = await session.execute(select(translation_language.c.language_iso639))
        langs = [item["language_iso639"] for item in result.mappings().all()]

        for obj in objs:
            print(obj["name"])
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
                    print(f"На слове {obj['name']} упала ошибка {HTTPError}")
    return data


async def main():
    data = await get_translations("country", country)
    await insert_data(data, translation)


# todo переделать в формат скрипта с параметрами запуска
asyncio.run(main())
