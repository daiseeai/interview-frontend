from pydantic import BaseModel
from datetime import datetime

class FilmActor(BaseModel):
    actor_id: int
    film_id: int
    last_update: datetime

    class Config:
        from_attributes = True
