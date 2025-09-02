from pydantic import BaseModel
from datetime import datetime

class Inventory(BaseModel):
    inventory_id: int
    film_id: int
    store_id: int
    last_update: datetime

    class Config:
        from_attributes = True
