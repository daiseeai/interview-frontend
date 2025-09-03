from fastapi import APIRouter, HTTPException
from typing import List
from src.schemas.country import Country
from src.utils.database import db_connection

router = APIRouter()

@router.get("/countries", response_model=List[Country])
async def get_countries(limit: int = 100, offset: int = 0):
    """Get all countries with pagination"""
    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT country_id, country, last_update FROM country ORDER BY country_id LIMIT %s OFFSET %s",
                    (limit, offset)
                )
                countries = []
                for row in cur.fetchall():
                    countries.append(Country(
                        country_id=row[0],
                        country=row[1],
                        last_update=row[2]
                    ))
                return countries
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/countries/{country_id}", response_model=Country)
async def get_country(country_id: int):
    """Get a specific country by ID"""
    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT country_id, country, last_update FROM country WHERE country_id = %s",
                    (country_id,)
                )
                row = cur.fetchone()
                if not row:
                    raise HTTPException(status_code=404, detail="Country not found")
                
                return Country(
                    country_id=row[0],
                    country=row[1],
                    last_update=row[2]
                )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
