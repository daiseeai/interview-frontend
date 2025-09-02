from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Rental(BaseModel):
    rental_id: int
    rental_date: datetime
    inventory_id: int
    customer_id: int
    return_date: Optional[datetime] = None
    staff_id: int
    last_update: datetime

    class Config:
        from_attributes = True
