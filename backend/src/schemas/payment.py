from pydantic import BaseModel
from datetime import datetime

class Payment(BaseModel):
    payment_id: int
    customer_id: int
    staff_id: int
    rental_id: int
    amount: float
    payment_date: datetime

    class Config:
        from_attributes = True
