from pydantic import BaseModel
from datetime import datetime

class Store(BaseModel):
    store_id: int
    manager_staff_id: int
    address_id: int
    last_update: datetime

    class Config:
        from_attributes = True
