from fastapi import APIRouter, HTTPException
from typing import List
from src.schemas.category import Category
from src.utils.database import db_connection

router = APIRouter()

@router.get("/categories", response_model=List[Category])
async def get_categories(limit: int = 100, offset: int = 0):
    """Get all categories with pagination"""
    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT category_id, name, last_update FROM category ORDER BY category_id LIMIT %s OFFSET %s",
                    (limit, offset)
                )
                categories = []
                for row in cur.fetchall():
                    categories.append(Category(
                        category_id=row[0],
                        name=row[1],
                        last_update=row[2]
                    ))
                return categories
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/categories/{category_id}", response_model=Category)
async def get_category(category_id: int):
    """Get a specific category by ID"""
    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT category_id, name, last_update FROM category WHERE category_id = %s",
                    (category_id,)
                )
                row = cur.fetchone()
                if not row:
                    raise HTTPException(status_code=404, detail="Category not found")
                
                return Category(
                    category_id=row[0],
                    name=row[1],
                    last_update=row[2]
                )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
