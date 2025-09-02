from pydantic import BaseModel
from datetime import datetime

class Country(BaseModel):
    country_id: int
    country: str
    last_update: datetime

    class Config:
        from_attributes = True
