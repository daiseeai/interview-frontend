from fastapi import APIRouter, HTTPException
from typing import List
from src.schemas.rental import Rental
from src.utils.database import db_connection

router = APIRouter()

@router.get("/rentals", response_model=List[Rental])
async def get_rentals(limit: int = 100, offset: int = 0):
    """Get all rentals with pagination"""
    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """SELECT rental_id, rental_date, inventory_id, customer_id, return_date, staff_id, last_update 
                       FROM rental ORDER BY rental_id LIMIT %s OFFSET %s""",
                    (limit, offset)
                )
                rentals = []
                for row in cur.fetchall():
                    rentals.append(Rental(
                        rental_id=row[0],
                        rental_date=row[1],
                        inventory_id=row[2],
                        customer_id=row[3],
                        return_date=row[4],
                        staff_id=row[5],
                        last_update=row[6]
                    ))
                return rentals
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/rentals/{rental_id}", response_model=Rental)
async def get_rental(rental_id: int):
    """Get a specific rental by ID"""
    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """SELECT rental_id, rental_date, inventory_id, customer_id, return_date, staff_id, last_update 
                       FROM rental WHERE rental_id = %s""",
                    (rental_id,)
                )
                row = cur.fetchone()
                if not row:
                    raise HTTPException(status_code=404, detail="Rental not found")
                
                return Rental(
                    rental_id=row[0],
                    rental_date=row[1],
                    inventory_id=row[2],
                    customer_id=row[3],
                    return_date=row[4],
                    staff_id=row[5],
                    last_update=row[6]
                )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/rentals/customer/{customer_id}", response_model=List[Rental])
async def get_rentals_by_customer(customer_id: int, limit: int = 100, offset: int = 0):
    """Get all rentals for a specific customer"""
    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """SELECT rental_id, rental_date, inventory_id, customer_id, return_date, staff_id, last_update 
                       FROM rental WHERE customer_id = %s ORDER BY rental_date DESC LIMIT %s OFFSET %s""",
                    (customer_id, limit, offset)
                )
                rentals = []
                for row in cur.fetchall():
                    rentals.append(Rental(
                        rental_id=row[0],
                        rental_date=row[1],
                        inventory_id=row[2],
                        customer_id=row[3],
                        return_date=row[4],
                        staff_id=row[5],
                        last_update=row[6]
                    ))
                return rentals
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.post("/rentals", response_model=Rental)
async def create_rental(rental: Rental):
    """Create a new rental"""
    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """INSERT INTO rental (rental_date, inventory_id, customer_id, return_date, staff_id, last_update) 
                       VALUES (%s, %s, %s, %s, %s, %s) RETURNING rental_id""",
                    (rental.rental_date, rental.inventory_id, rental.customer_id, rental.return_date, 
                     rental.staff_id, rental.last_update)
                )
                rental_id = cur.fetchone()[0]
                conn.commit()
                
                return Rental(
                    rental_id=rental_id,
                    rental_date=rental.rental_date,
                    inventory_id=rental.inventory_id,
                    customer_id=rental.customer_id,
                    return_date=rental.return_date,
                    staff_id=rental.staff_id,
                    last_update=rental.last_update
                )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.put("/rentals/{rental_id}", response_model=Rental)
async def update_rental(rental_id: int, rental: Rental):
    """Update an existing rental"""
    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """UPDATE rental SET rental_date = %s, inventory_id = %s, customer_id = %s, 
                       return_date = %s, staff_id = %s, last_update = %s WHERE rental_id = %s""",
                    (rental.rental_date, rental.inventory_id, rental.customer_id, rental.return_date,
                     rental.staff_id, rental.last_update, rental_id)
                )
                if cur.rowcount == 0:
                    raise HTTPException(status_code=404, detail="Rental not found")
                conn.commit()
                
                return Rental(
                    rental_id=rental_id,
                    rental_date=rental.rental_date,
                    inventory_id=rental.inventory_id,
                    customer_id=rental.customer_id,
                    return_date=rental.return_date,
                    staff_id=rental.staff_id,
                    last_update=rental.last_update
                )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.delete("/rentals/{rental_id}")
async def delete_rental(rental_id: int):
    """Delete a rental"""
    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM rental WHERE rental_id = %s", (rental_id,))
                if cur.rowcount == 0:
                    raise HTTPException(status_code=404, detail="Rental not found")
                conn.commit()
                return {"status": 200, "message": "Rental deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.put("/rentals/{rental_id}/return")
async def return_rental(rental_id: int):
    """Mark a rental as returned (set return_date to current timestamp)"""
    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE rental SET return_date = NOW(), last_update = NOW() WHERE rental_id = %s AND return_date IS NULL",
                    (rental_id,)
                )
                if cur.rowcount == 0:
                    raise HTTPException(status_code=404, detail="Rental not found or already returned")
                conn.commit()
                return {"status": 200, "message": "Rental returned successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
