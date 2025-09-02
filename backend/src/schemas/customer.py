from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class Customer(BaseModel):
    customer_id: int
    store_id: int
    first_name: str
    last_name: str
    email: Optional[str] = None
    address_id: int
    activebool: bool = True
    create_date: date
    last_update: Optional[datetime] = None
    active: Optional[int] = None

    class Config:
        from_attributes = True