from pydantic import BaseModel
from datetime import datetime

class Category(BaseModel):
    category_id: int
    name: str
    last_update: datetime

    class Config:
        from_attributes = True
