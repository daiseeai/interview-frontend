from pydantic import BaseModel
from datetime import datetime

class Language(BaseModel):
    language_id: int
    name: str
    last_update: datetime

    class Config:
        from_attributes = True
