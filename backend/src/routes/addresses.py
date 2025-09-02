from fastapi import APIRouter, HTTPException
from typing import List
from src.schemas.address import Address
from src.utils.database import db_connection

router = APIRouter()

@router.get("/addresses", response_model=List[Address])
async def get_addresses(limit: int = 100, offset: int = 0):
    """Get all addresses with pagination"""
    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """SELECT address_id, address, address2, district, city_id, postal_code, phone, last_update 
                       FROM address ORDER BY address_id LIMIT %s OFFSET %s""",
                    (limit, offset)
                )
                addresses = []
                for row in cur.fetchall():
                    addresses.append(Address(
                        address_id=row[0],
                        address=row[1],
                        address2=row[2],
                        district=row[3],
                        city_id=row[4],
                        postal_code=row[5],
                        phone=row[6],
                        last_update=row[7]
                    ))
                return addresses
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/addresses/{address_id}", response_model=Address)
async def get_address(address_id: int):
    """Get a specific address by ID"""
    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """SELECT address_id, address, address2, district, city_id, postal_code, phone, last_update 
                       FROM address WHERE address_id = %s""",
                    (address_id,)
                )
                row = cur.fetchone()
                if not row:
                    raise HTTPException(status_code=404, detail="Address not found")
                
                return Address(
                    address_id=row[0],
                    address=row[1],
                    address2=row[2],
                    district=row[3],
                    city_id=row[4],
                    postal_code=row[5],
                    phone=row[6],
                    last_update=row[7]
                )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
