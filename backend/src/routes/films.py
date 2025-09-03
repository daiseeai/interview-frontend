from fastapi import APIRouter, HTTPException
from typing import List
from src.schemas.film import Film
from src.utils.database import db_connection

router = APIRouter()

@router.get("/films", response_model=List[Film])
async def get_films(limit: int = 100, offset: int = 0):
    """Get all films with pagination"""
    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """SELECT film_id, title, description, release_year, language_id, original_language_id, 
                       rental_duration, rental_rate, length, replacement_cost, rating, last_update, 
                       special_features, fulltext FROM film ORDER BY film_id LIMIT %s OFFSET %s""",
                    (limit, offset)
                )
                films = []
                for row in cur.fetchall():
                    films.append(Film(
                        film_id=row[0],
                        title=row[1],
                        description=row[2],
                        release_year=row[3],
                        language_id=row[4],
                        original_language_id=row[5],
                        rental_duration=row[6],
                        rental_rate=row[7],
                        length=row[8],
                        replacement_cost=row[9],
                        rating=row[10],
                        last_update=row[11],
                        special_features=row[12],
                        fulltext=row[13]
                    ))
                return films
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/films/{film_id}", response_model=Film)
async def get_film(film_id: int):
    """Get a specific film by ID"""
    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """SELECT film_id, title, description, release_year, language_id, original_language_id, 
                       rental_duration, rental_rate, length, replacement_cost, rating, last_update, 
                       special_features, fulltext FROM film WHERE film_id = %s""",
                    (film_id,)
                )
                row = cur.fetchone()
                if not row:
                    raise HTTPException(status_code=404, detail="Film not found")
                
                return Film(
                    film_id=row[0],
                    title=row[1],
                    description=row[2],
                    release_year=row[3],
                    language_id=row[4],
                    original_language_id=row[5],
                    rental_duration=row[6],
                    rental_rate=row[7],
                    length=row[8],
                    replacement_cost=row[9],
                    rating=row[10],
                    last_update=row[11],
                    special_features=row[12],
                    fulltext=row[13]
                )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.post("/films", response_model=Film)
async def create_film(film: Film):
    """Create a new film"""
    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """INSERT INTO film (title, description, release_year, language_id, original_language_id, 
                       rental_duration, rental_rate, length, replacement_cost, rating, last_update, 
                       special_features, fulltext) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING film_id""",
                    (film.title, film.description, film.release_year, film.language_id, film.original_language_id,
                     film.rental_duration, film.rental_rate, film.length, film.replacement_cost, film.rating,
                     film.last_update, film.special_features, film.fulltext)
                )
                film_id = cur.fetchone()[0]
                conn.commit()
                
                return Film(
                    film_id=film_id,
                    title=film.title,
                    description=film.description,
                    release_year=film.release_year,
                    language_id=film.language_id,
                    original_language_id=film.original_language_id,
                    rental_duration=film.rental_duration,
                    rental_rate=film.rental_rate,
                    length=film.length,
                    replacement_cost=film.replacement_cost,
                    rating=film.rating,
                    last_update=film.last_update,
                    special_features=film.special_features,
                    fulltext=film.fulltext
                )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.put("/films/{film_id}", response_model=Film)
async def update_film(film_id: int, film: Film):
    """Update an existing film"""
    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """UPDATE film SET title = %s, description = %s, release_year = %s, language_id = %s, 
                       original_language_id = %s, rental_duration = %s, rental_rate = %s, length = %s, 
                       replacement_cost = %s, rating = %s, last_update = %s, special_features = %s, 
                       fulltext = %s WHERE film_id = %s""",
                    (film.title, film.description, film.release_year, film.language_id, film.original_language_id,
                     film.rental_duration, film.rental_rate, film.length, film.replacement_cost, film.rating,
                     film.last_update, film.special_features, film.fulltext, film_id)
                )
                if cur.rowcount == 0:
                    raise HTTPException(status_code=404, detail="Film not found")
                conn.commit()
                
                return Film(
                    film_id=film_id,
                    title=film.title,
                    description=film.description,
                    release_year=film.release_year,
                    language_id=film.language_id,
                    original_language_id=film.original_language_id,
                    rental_duration=film.rental_duration,
                    rental_rate=film.rental_rate,
                    length=film.length,
                    replacement_cost=film.replacement_cost,
                    rating=film.rating,
                    last_update=film.last_update,
                    special_features=film.special_features,
                    fulltext=film.fulltext
                )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.delete("/films/{film_id}")
async def delete_film(film_id: int):
    """Delete a film"""
    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM film WHERE film_id = %s", (film_id,))
                if cur.rowcount == 0:
                    raise HTTPException(status_code=404, detail="Film not found")
                conn.commit()
                return {"status": 200, "message": "Film deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
