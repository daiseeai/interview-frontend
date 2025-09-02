from fastapi import APIRouter, HTTPException
from typing import List
from src.schemas.views import (
    ActorInfo, CustomerList, FilmList, NicerButSlowerFilmList, 
    SalesByFilmCategory, SalesByStore, StaffList
)
from src.utils.database import db_connection

router = APIRouter()

@router.get("/views/actor-info", response_model=List[ActorInfo])
async def get_actor_info(limit: int = 100, offset: int = 0):
    """Get actor information view"""
    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT actor_id, first_name, last_name, film_info FROM actor_info ORDER BY actor_id LIMIT %s OFFSET %s",
                    (limit, offset)
                )
                actors = []
                for row in cur.fetchall():
                    actors.append(ActorInfo(
                        actor_id=row[0],
                        first_name=row[1],
                        last_name=row[2],
                        film_info=row[3]
                    ))
                return actors
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/views/customer-list", response_model=List[CustomerList])
async def get_customer_list(limit: int = 100, offset: int = 0):
    """Get customer list view"""
    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """SELECT id, name, address, "zip code", phone, city, country, notes, sid 
                       FROM customer_list ORDER BY id LIMIT %s OFFSET %s""",
                    (limit, offset)
                )
                customers = []
                for row in cur.fetchall():
                    customers.append(CustomerList(
                        id=row[0],
                        name=row[1],
                        address=row[2],
                        zip_code=row[3],
                        phone=row[4],
                        city=row[5],
                        country=row[6],
                        notes=row[7],
                        sid=row[8]
                    ))
                return customers
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/views/film-list", response_model=List[FilmList])
async def get_film_list(limit: int = 100, offset: int = 0):
    """Get film list view"""
    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT fid, title, description, category, price, length, rating, actors FROM film_list ORDER BY fid LIMIT %s OFFSET %s",
                    (limit, offset)
                )
                films = []
                for row in cur.fetchall():
                    films.append(FilmList(
                        fid=row[0],
                        title=row[1],
                        description=row[2],
                        category=row[3],
                        price=row[4],
                        length=row[5],
                        rating=row[6],
                        actors=row[7]
                    ))
                return films
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/views/nicer-film-list", response_model=List[NicerButSlowerFilmList])
async def get_nicer_film_list(limit: int = 100, offset: int = 0):
    """Get nicer but slower film list view"""
    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT fid, title, description, category, price, length, rating, actors FROM nicer_but_slower_film_list ORDER BY fid LIMIT %s OFFSET %s",
                    (limit, offset)
                )
                films = []
                for row in cur.fetchall():
                    films.append(NicerButSlowerFilmList(
                        fid=row[0],
                        title=row[1],
                        description=row[2],
                        category=row[3],
                        price=row[4],
                        length=row[5],
                        rating=row[6],
                        actors=row[7]
                    ))
                return films
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/views/sales-by-film-category", response_model=List[SalesByFilmCategory])
async def get_sales_by_film_category(limit: int = 100, offset: int = 0):
    """Get sales by film category view"""
    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT category, total_sales FROM sales_by_film_category ORDER BY total_sales DESC LIMIT %s OFFSET %s", (limit, offset))
                sales = []
                for row in cur.fetchall():
                    sales.append(SalesByFilmCategory(
                        category=row[0],
                        total_sales=row[1]
                    ))
                return sales
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/views/sales-by-store", response_model=List[SalesByStore])
async def get_sales_by_store(limit: int = 100, offset: int = 0):
    """Get sales by store view"""
    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT store, manager, total_sales FROM sales_by_store ORDER BY total_sales DESC LIMIT %s OFFSET %s", (limit, offset))
                sales = []
                for row in cur.fetchall():
                    sales.append(SalesByStore(
                        store=row[0],
                        manager=row[1],
                        total_sales=row[2]
                    ))
                return sales
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/views/staff-list", response_model=List[StaffList])
async def get_staff_list(limit: int = 100, offset: int = 0):
    """Get staff list view"""
    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """SELECT id, name, address, "zip code", phone, city, country, sid 
                       FROM staff_list ORDER BY id LIMIT %s OFFSET %s""",
                    (limit, offset)
                )
                staff = []
                for row in cur.fetchall():
                    staff.append(StaffList(
                        id=row[0],
                        name=row[1],
                        address=row[2],
                        zip_code=row[3],
                        phone=row[4],
                        city=row[5],
                        country=row[6],
                        sid=row[7]
                    ))
                return staff
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
