from datetime import datetime
from pydantic import BaseModel

class TranslateRead(BaseModel):
    entity: str
    entity_id: int
    language: str
    translate: str
    last_updated_at: datetime

class TranslateCreate(BaseModel):
    entity: str
    entity_id: int
    language: str
    translate: str

class TranslateUpdate(BaseModel):
    translate: str