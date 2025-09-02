from fastapi import APIRouter, HTTPException
from typing import List
from src.schemas.payment import Payment
from src.utils.database import db_connection

router = APIRouter()

@router.get("/payments", response_model=List[Payment])
async def get_payments(limit: int = 100, offset: int = 0):
    """Get all payments with pagination"""
    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """SELECT payment_id, customer_id, staff_id, rental_id, amount, payment_date 
                       FROM payment ORDER BY payment_date DESC LIMIT %s OFFSET %s""",
                    (limit, offset)
                )
                payments = []
                for row in cur.fetchall():
                    payments.append(Payment(
                        payment_id=row[0],
                        customer_id=row[1],
                        staff_id=row[2],
                        rental_id=row[3],
                        amount=row[4],
                        payment_date=row[5]
                    ))
                return payments
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/payments/{payment_id}", response_model=Payment)
async def get_payment(payment_id: int):
    """Get a specific payment by ID"""
    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """SELECT payment_id, customer_id, staff_id, rental_id, amount, payment_date 
                       FROM payment WHERE payment_id = %s""",
                    (payment_id,)
                )
                row = cur.fetchone()
                if not row:
                    raise HTTPException(status_code=404, detail="Payment not found")
                
                return Payment(
                    payment_id=row[0],
                    customer_id=row[1],
                    staff_id=row[2],
                    rental_id=row[3],
                    amount=row[4],
                    payment_date=row[5]
                )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/payments/customer/{customer_id}", response_model=List[Payment])
async def get_payments_by_customer(customer_id: int, limit: int = 100, offset: int = 0):
    """Get all payments for a specific customer"""
    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """SELECT payment_id, customer_id, staff_id, rental_id, amount, payment_date 
                       FROM payment WHERE customer_id = %s ORDER BY payment_date DESC LIMIT %s OFFSET %s""",
                    (customer_id, limit, offset)
                )
                payments = []
                for row in cur.fetchall():
                    payments.append(Payment(
                        payment_id=row[0],
                        customer_id=row[1],
                        staff_id=row[2],
                        rental_id=row[3],
                        amount=row[4],
                        payment_date=row[5]
                    ))
                return payments
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/payments/rental/{rental_id}", response_model=List[Payment])
async def get_payments_by_rental(rental_id: int, limit: int = 100, offset: int = 0):
    """Get all payments for a specific rental"""
    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """SELECT payment_id, customer_id, staff_id, rental_id, amount, payment_date 
                       FROM payment WHERE rental_id = %s ORDER BY payment_date LIMIT %s OFFSET %s""",
                    (rental_id, limit, offset)
                )
                payments = []
                for row in cur.fetchall():
                    payments.append(Payment(
                        payment_id=row[0],
                        customer_id=row[1],
                        staff_id=row[2],
                        rental_id=row[3],
                        amount=row[4],
                        payment_date=row[5]
                    ))
                return payments
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.post("/payments", response_model=Payment)
async def create_payment(payment: Payment):
    """Create a new payment"""
    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """INSERT INTO payment (customer_id, staff_id, rental_id, amount, payment_date) 
                       VALUES (%s, %s, %s, %s, %s) RETURNING payment_id""",
                    (payment.customer_id, payment.staff_id, payment.rental_id, payment.amount, payment.payment_date)
                )
                payment_id = cur.fetchone()[0]
                conn.commit()
                
                return Payment(
                    payment_id=payment_id,
                    customer_id=payment.customer_id,
                    staff_id=payment.staff_id,
                    rental_id=payment.rental_id,
                    amount=payment.amount,
                    payment_date=payment.payment_date
                )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.put("/payments/{payment_id}", response_model=Payment)
async def update_payment(payment_id: int, payment: Payment):
    """Update an existing payment"""
    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """UPDATE payment SET customer_id = %s, staff_id = %s, rental_id = %s, 
                       amount = %s, payment_date = %s WHERE payment_id = %s""",
                    (payment.customer_id, payment.staff_id, payment.rental_id, payment.amount, 
                     payment.payment_date, payment_id)
                )
                if cur.rowcount == 0:
                    raise HTTPException(status_code=404, detail="Payment not found")
                conn.commit()
                
                return Payment(
                    payment_id=payment_id,
                    customer_id=payment.customer_id,
                    staff_id=payment.staff_id,
                    rental_id=payment.rental_id,
                    amount=payment.amount,
                    payment_date=payment.payment_date
                )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.delete("/payments/{payment_id}")
async def delete_payment(payment_id: int):
    """Delete a payment"""
    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM payment WHERE payment_id = %s", (payment_id,))
                if cur.rowcount == 0:
                    raise HTTPException(status_code=404, detail="Payment not found")
                conn.commit()
                return {"status": 200, "message": "Payment deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/payments/customer/{customer_id}/total")
async def get_customer_total_payments(customer_id: int):
    """Get total amount paid by a customer"""
    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT COALESCE(SUM(amount), 0) FROM payment WHERE customer_id = %s",
                    (customer_id,)
                )
                total = cur.fetchone()[0]
                return {"customer_id": customer_id, "total_payments": float(total)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
