from fastapi import APIRouter, HTTPException
from typing import List
from src.schemas.city import City
from src.utils.database import db_connection

router = APIRouter()

@router.get("/cities", response_model=List[City])
async def get_cities(limit: int = 100, offset: int = 0):
    """Get all cities with pagination"""
    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT city_id, city, country_id, last_update FROM city ORDER BY city_id LIMIT %s OFFSET %s",
                    (limit, offset)
                )
                cities = []
                for row in cur.fetchall():
                    cities.append(City(
                        city_id=row[0],
                        city=row[1],
                        country_id=row[2],
                        last_update=row[3]
                    ))
                return cities
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/cities/{city_id}", response_model=City)
async def get_city(city_id: int):
    """Get a specific city by ID"""
    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT city_id, city, country_id, last_update FROM city WHERE city_id = %s",
                    (city_id,)
                )
                row = cur.fetchone()
                if not row:
                    raise HTTPException(status_code=404, detail="City not found")
                
                return City(
                    city_id=row[0],
                    city=row[1],
                    country_id=row[2],
                    last_update=row[3]
                )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/cities/country/{country_id}", response_model=List[City])
async def get_cities_by_country(country_id: int, limit: int = 100, offset: int = 0):
    """Get all cities for a specific country"""
    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT city_id, city, country_id, last_update FROM city WHERE country_id = %s ORDER BY city LIMIT %s OFFSET %s",
                    (country_id, limit, offset)
                )
                cities = []
                for row in cur.fetchall():
                    cities.append(City(
                        city_id=row[0],
                        city=row[1],
                        country_id=row[2],
                        last_update=row[3]
                    ))
                return cities
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
