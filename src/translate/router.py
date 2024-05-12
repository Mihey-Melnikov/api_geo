from typing import List
from fastapi import APIRouter, Depends, Request
from sqlalchemy import update, select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from src.translate.models import translate, language
from src.translate.schemas import Language, TranslateCreate, TranslateRead, TranslateUpdate
from logger.logger import get_api_logger


router = APIRouter(
    prefix="/api/translate",
    tags=["Translate"]
)

@router.get("/", response_model=List[TranslateRead])
async def get_translate_by_id(
    request: Request,
    entity: str, 
    entity_id: int, 
    session: AsyncSession = Depends(get_async_session)):
    """
    Get all translations about entity by entity name and ID.
    """
    query = select(translate) \
            .where(translate.c.entity == entity, translate.c.entity_id == entity_id)
    result = await session.execute(query)
    data = result.mappings().all()
    logger = get_api_logger(str(request.url))
    logger.info(data)
    return data

@router.post("/", response_model=List[TranslateRead])
async def add_translate(
    request: Request,
    new_translate: List[TranslateCreate], 
    session: AsyncSession = Depends(get_async_session)):
    """
    Create a new translate.
    """
    query = insert(translate) \
            .values([item.model_dump() for item in new_translate]) \
            .returning(translate)
    result = await session.execute(query)
    await session.commit()
    data = result.mappings().all()
    logger = get_api_logger(str(request.url))
    logger.info(data)
    return data

@router.delete("/", response_model=List[TranslateRead])
async def delete_translate(
    request: Request,
    entity: str,
    entity_id: int,
    session: AsyncSession = Depends(get_async_session)):
    """
    Delete all translations about entity by entity name and ID.
    """
    query = delete(translate) \
            .where(translate.c.entity == entity, translate.c.entity_id == entity_id) \
            .returning(translate)
    result = await session.execute(query)
    await session.commit()
    data = result.mappings().all()
    logger = get_api_logger(str(request.url))
    logger.info(data)
    return data

@router.patch("/", response_model=TranslateRead)
async def update_translate(
    request: Request,
    entity: str,
    entity_id: int,
    language: str,
    updated_rows: TranslateUpdate,
    session: AsyncSession = Depends(get_async_session)):
    """
    Change the translate.
    """
    query = update(translate) \
            .where(translate.c.entity == entity, translate.c.entity_id == entity_id, translate.c.language == language) \
            .values(updated_rows.model_dump(exclude_unset=True)) \
            .returning(translate)
    result = await session.execute(query)
    await session.commit()
    data = result.one_or_none()
    logger = get_api_logger(str(request.url))
    logger.info(data)
    return data

@router.get("/language", response_model=List[Language])
async def get_languages(
    request: Request,
    session: AsyncSession = Depends(get_async_session)):
    """
    Get all languages to translate.
    """
    query = select(language)
    result = await session.execute(query)
    data = result.mappings().all()
    logger = get_api_logger(str(request.url))
    logger.info(data)
    return data

@router.post("/language", response_model=Language)
async def add_languages(
    request: Request,
    new_language: Language,
    session: AsyncSession = Depends(get_async_session)):
    """
    Add a new language.
    """
    query = insert(language) \
            .values(new_language.model_dump()) \
            .returning(language)
    result = await session.execute(query)
    await session.commit()
    data = result.one()
    logger = get_api_logger(str(request.url))
    logger.info(data)
    return data

@router.delete("/language", response_model=Language)
async def delete_languages(
    request: Request,
    language_iso639: str,
    session: AsyncSession = Depends(get_async_session)):
    """
    Delete all translations about entity by entity name and ID.
    """
    query = delete(language) \
            .where(language.c.language_iso639 == language_iso639) \
            .returning(language)
    result = await session.execute(query)
    await session.commit()
    data = result.one()
    logger = get_api_logger(str(request.url))
    logger.info(data)
    return data
