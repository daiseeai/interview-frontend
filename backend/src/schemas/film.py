from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum

class MpaaRating(str, Enum):
    G = "G"
    PG = "PG"
    PG_13 = "PG-13"
    R = "R"
    NC_17 = "NC-17"

class Film(BaseModel):
    film_id: int
    title: str
    description: Optional[str] = None
    release_year: Optional[int] = None
    language_id: int
    original_language_id: Optional[int] = None
    rental_duration: int = 3
    rental_rate: float = 4.99
    length: Optional[int] = None
    replacement_cost: float = 19.99
    rating: MpaaRating = MpaaRating.G
    last_update: datetime
    special_features: Optional[List[str]] = None
    fulltext: str

    class Config:
        from_attributes = True
