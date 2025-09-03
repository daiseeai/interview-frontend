from fastapi import APIRouter, HTTPException
from typing import List
from src.schemas.inventory import Inventory
from src.utils.database import db_connection

router = APIRouter()

@router.get("/inventory", response_model=List[Inventory])
async def get_inventory(limit: int = 100, offset: int = 0):
    """Get all inventory items with pagination"""
    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT inventory_id, film_id, store_id, last_update FROM inventory ORDER BY inventory_id LIMIT %s OFFSET %s",
                    (limit, offset)
                )
                inventory_items = []
                for row in cur.fetchall():
                    inventory_items.append(Inventory(
                        inventory_id=row[0],
                        film_id=row[1],
                        store_id=row[2],
                        last_update=row[3]
                    ))
                return inventory_items
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/inventory/{inventory_id}", response_model=Inventory)
async def get_inventory_item(inventory_id: int):
    """Get a specific inventory item by ID"""
    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT inventory_id, film_id, store_id, last_update FROM inventory WHERE inventory_id = %s",
                    (inventory_id,)
                )
                row = cur.fetchone()
                if not row:
                    raise HTTPException(status_code=404, detail="Inventory item not found")
                
                return Inventory(
                    inventory_id=row[0],
                    film_id=row[1],
                    store_id=row[2],
                    last_update=row[3]
                )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/inventory/film/{film_id}", response_model=List[Inventory])
async def get_inventory_by_film(film_id: int, limit: int = 100, offset: int = 0):
    """Get all inventory items for a specific film"""
    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT inventory_id, film_id, store_id, last_update FROM inventory WHERE film_id = %s ORDER BY inventory_id LIMIT %s OFFSET %s",
                    (film_id, limit, offset)
                )
                inventory_items = []
                for row in cur.fetchall():
                    inventory_items.append(Inventory(
                        inventory_id=row[0],
                        film_id=row[1],
                        store_id=row[2],
                        last_update=row[3]
                    ))
                return inventory_items
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/inventory/store/{store_id}", response_model=List[Inventory])
async def get_inventory_by_store(store_id: int, limit: int = 100, offset: int = 0):
    """Get all inventory items for a specific store"""
    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT inventory_id, film_id, store_id, last_update FROM inventory WHERE store_id = %s ORDER BY inventory_id LIMIT %s OFFSET %s",
                    (store_id, limit, offset)
                )
                inventory_items = []
                for row in cur.fetchall():
                    inventory_items.append(Inventory(
                        inventory_id=row[0],
                        film_id=row[1],
                        store_id=row[2],
                        last_update=row[3]
                    ))
                return inventory_items
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
