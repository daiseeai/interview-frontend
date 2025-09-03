from fastapi import APIRouter, HTTPException
from typing import List
from src.schemas.language import Language
from src.utils.database import db_connection

router = APIRouter()

@router.get("/languages", response_model=List[Language])
async def get_languages(limit: int = 100, offset: int = 0):
    """Get all languages with pagination"""
    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT language_id, name, last_update FROM language ORDER BY language_id LIMIT %s OFFSET %s",
                    (limit, offset)
                )
                languages = []
                for row in cur.fetchall():
                    languages.append(Language(
                        language_id=row[0],
                        name=row[1],
                        last_update=row[2]
                    ))
                return languages
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/languages/{language_id}", response_model=Language)
async def get_language(language_id: int):
    """Get a specific language by ID"""
    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT language_id, name, last_update FROM language WHERE language_id = %s",
                    (language_id,)
                )
                row = cur.fetchone()
                if not row:
                    raise HTTPException(status_code=404, detail="Language not found")
                
                return Language(
                    language_id=row[0],
                    name=row[1],
                    last_update=row[2]
                )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
