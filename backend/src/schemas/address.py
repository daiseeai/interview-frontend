from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Address(BaseModel):
    address_id: int
    address: str
    address2: Optional[str] = None
    district: str
    city_id: int
    postal_code: Optional[str] = None
    phone: str
    last_update: datetime

    class Config:
        from_attributes = True
