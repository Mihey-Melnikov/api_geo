from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy import update, select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.translate.models import translation as translate
from src.translate.schemas import TranslateCreate, TranslateRead, TranslateUpdate

router = APIRouter(
    prefix="/translate",
    tags=["Translate"]
)

@router.get("/", response_model=List[TranslateRead])
async def get_translate_by_id(entity: str, entity_id: int, session: AsyncSession = Depends(get_async_session)):
    """
    Get all translations about entity by entity name and ID.
    """
    query = select(translate) \
            .where(translate.c.entity == entity, translate.c.entity_id == entity_id)
    result = await session.execute(query)
    return result.mappings().all()

@router.post("/", response_model=List[TranslateRead])
async def add_translate(new_translate: List[TranslateCreate], session: AsyncSession = Depends(get_async_session)):
    """
    Create a new translate.
    """
    query = insert(translate) \
            .values([item.model_dump() for item in new_translate]) \
            .returning(translate)
    result = await session.execute(query)
    await session.commit()
    return result.mappings().all()

@router.delete("/", response_model=List[TranslateRead])
async def delete_translate(entity: str, entity_id: int, session: AsyncSession = Depends(get_async_session)):
    """
    Delete all translations about entity by entity name and ID.
    """
    query = delete(translate) \
            .where(translate.c.entity == entity, translate.c.entity_id == entity_id) \
            .returning(translate)
    result = await session.execute(query)
    await session.commit()
    return result.mappings().all()

@router.patch("/", response_model=List[TranslateRead])
async def update_translate(entity: str, entity_id: int, updated_rows: List[TranslateUpdate], session: AsyncSession = Depends(get_async_session)):
    """
    Change the translate.
    """
    query = update(translate) \
            .where(translate.c.entity == entity, translate.c.entity_id == entity_id) \
            .values(updated_rows.model_dump(exclude_unset=True)) \
            .returning(translate)
    result = await session.execute(query)
    await session.commit()
    return result.one_or_none()