from pydantic import BaseModel
from typing import Optional
from .film import MpaaRating

class ActorInfo(BaseModel):
    actor_id: int
    first_name: str
    last_name: str
    film_info: Optional[str] = None

    class Config:
        from_attributes = True

class CustomerList(BaseModel):
    id: int
    name: str
    address: str
    zip_code: Optional[str] = None
    phone: str
    city: str
    country: str
    notes: str
    sid: int

    class Config:
        from_attributes = True

class FilmList(BaseModel):
    fid: int
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    price: float
    length: Optional[int] = None
    rating: MpaaRating
    actors: Optional[str] = None

    class Config:
        from_attributes = True

class NicerButSlowerFilmList(BaseModel):
    fid: int
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    price: float
    length: Optional[int] = None
    rating: MpaaRating
    actors: Optional[str] = None

    class Config:
        from_attributes = True

class SalesByFilmCategory(BaseModel):
    category: str
    total_sales: float

    class Config:
        from_attributes = True

class SalesByStore(BaseModel):
    store: str
    manager: str
    total_sales: float

    class Config:
        from_attributes = True

class StaffList(BaseModel):
    id: int
    name: str
    address: str
    zip_code: Optional[str] = None
    phone: str
    city: str
    country: str
    sid: int

    class Config:
        from_attributes = True
