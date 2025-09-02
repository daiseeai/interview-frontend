from fastapi import APIRouter, HTTPException
from typing import List
from src.schemas.staff import Staff
from src.utils.database import db_connection

router = APIRouter()

@router.get("/staff", response_model=List[Staff])
async def get_staff(limit: int = 100, offset: int = 0):
    """Get all staff with pagination"""
    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """SELECT staff_id, first_name, last_name, address_id, email, store_id, active, 
                       username, password, last_update, picture FROM staff ORDER BY staff_id LIMIT %s OFFSET %s""",
                    (limit, offset)
                )
                staff_list = []
                for row in cur.fetchall():
                    staff_list.append(Staff(
                        staff_id=row[0],
                        first_name=row[1],
                        last_name=row[2],
                        address_id=row[3],
                        email=row[4],
                        store_id=row[5],
                        active=row[6],
                        username=row[7],
                        password=row[8],
                        last_update=row[9],
                        picture=row[10]
                    ))
                return staff_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/staff/{staff_id}", response_model=Staff)
async def get_staff_member(staff_id: int):
    """Get a specific staff member by ID"""
    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """SELECT staff_id, first_name, last_name, address_id, email, store_id, active, 
                       username, password, last_update, picture FROM staff WHERE staff_id = %s""",
                    (staff_id,)
                )
                row = cur.fetchone()
                if not row:
                    raise HTTPException(status_code=404, detail="Staff member not found")
                
                return Staff(
                    staff_id=row[0],
                    first_name=row[1],
                    last_name=row[2],
                    address_id=row[3],
                    email=row[4],
                    store_id=row[5],
                    active=row[6],
                    username=row[7],
                    password=row[8],
                    last_update=row[9],
                    picture=row[10]
                )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/staff/store/{store_id}", response_model=List[Staff])
async def get_staff_by_store(store_id: int, limit: int = 100, offset: int = 0):
    """Get all staff for a specific store"""
    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """SELECT staff_id, first_name, last_name, address_id, email, store_id, active, 
                       username, password, last_update, picture FROM staff WHERE store_id = %s ORDER BY staff_id LIMIT %s OFFSET %s""",
                    (store_id, limit, offset)
                )
                staff_list = []
                for row in cur.fetchall():
                    staff_list.append(Staff(
                        staff_id=row[0],
                        first_name=row[1],
                        last_name=row[2],
                        address_id=row[3],
                        email=row[4],
                        store_id=row[5],
                        active=row[6],
                        username=row[7],
                        password=row[8],
                        last_update=row[9],
                        picture=row[10]
                    ))
                return staff_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
