from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Staff(BaseModel):
    staff_id: int
    first_name: str
    last_name: str
    address_id: int
    email: Optional[str] = None
    store_id: int
    active: bool = True
    username: str
    password: Optional[str] = None
    last_update: datetime
    picture: Optional[bytes] = None

    class Config:
        from_attributes = True
