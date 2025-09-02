from pydantic import BaseModel
from datetime import datetime

class FilmCategory(BaseModel):
    film_id: int
    category_id: int
    last_update: datetime

    class Config:
        from_attributes = True
