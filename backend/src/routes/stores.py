from fastapi import APIRouter, HTTPException
from typing import List
from src.schemas.store import Store
from src.utils.database import db_connection

router = APIRouter()

@router.get("/stores", response_model=List[Store])
async def get_stores(limit: int = 100, offset: int = 0):
    """Get all stores with pagination"""
    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT store_id, manager_staff_id, address_id, last_update FROM store ORDER BY store_id LIMIT %s OFFSET %s",
                    (limit, offset)
                )
                stores = []
                for row in cur.fetchall():
                    stores.append(Store(
                        store_id=row[0],
                        manager_staff_id=row[1],
                        address_id=row[2],
                        last_update=row[3]
                    ))
                return stores
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/stores/{store_id}", response_model=Store)
async def get_store(store_id: int):
    """Get a specific store by ID"""
    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT store_id, manager_staff_id, address_id, last_update FROM store WHERE store_id = %s",
                    (store_id,)
                )
                row = cur.fetchone()
                if not row:
                    raise HTTPException(status_code=404, detail="Store not found")
                
                return Store(
                    store_id=row[0],
                    manager_staff_id=row[1],
                    address_id=row[2],
                    last_update=row[3]
                )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
