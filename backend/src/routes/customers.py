from fastapi import APIRouter, HTTPException
from typing import List, Optional
from src.schemas.customer import Customer
from src.utils.database import db_connection

router = APIRouter()

@router.get("/customers", response_model=List[Customer])
async def get_customers(limit: int = 100, offset: int = 0):
    """Get all customers with pagination"""
    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT customer_id, store_id, first_name, last_name, email, address_id, activebool, create_date, last_update, active FROM customer ORDER BY customer_id LIMIT %s OFFSET %s",
                    (limit, offset)
                )
                customers = []
                for row in cur.fetchall():
                    customers.append(Customer(
                        customer_id=row[0],
                        store_id=row[1],
                        first_name=row[2],
                        last_name=row[3],
                        email=row[4],
                        address_id=row[5],
                        activebool=row[6],
                        create_date=row[7],
                        last_update=row[8],
                        active=row[9]
                    ))
                return customers
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/customers/{customer_id}", response_model=Customer)
async def get_customer(customer_id: int):
    """Get a specific customer by ID"""
    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT customer_id, store_id, first_name, last_name, email, address_id, activebool, create_date, last_update, active FROM customer WHERE customer_id = %s",
                    (customer_id,)
                )
                row = cur.fetchone()
                if not row:
                    raise HTTPException(status_code=404, detail="Customer not found")
                
                return Customer(
                    customer_id=row[0],
                    store_id=row[1],
                    first_name=row[2],
                    last_name=row[3],
                    email=row[4],
                    address_id=row[5],
                    activebool=row[6],
                    create_date=row[7],
                    last_update=row[8],
                    active=row[9]
                )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.post("/customers", response_model=Customer)
async def create_customer(customer: Customer):
    """Create a new customer"""
    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """INSERT INTO customer (store_id, first_name, last_name, email, address_id, activebool, create_date, last_update, active) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING customer_id""",
                    (customer.store_id, customer.first_name, customer.last_name, customer.email, 
                     customer.address_id, customer.activebool, customer.create_date, customer.last_update, customer.active)
                )
                customer_id = cur.fetchone()[0]
                conn.commit()
                
                return Customer(
                    customer_id=customer_id,
                    store_id=customer.store_id,
                    first_name=customer.first_name,
                    last_name=customer.last_name,
                    email=customer.email,
                    address_id=customer.address_id,
                    activebool=customer.activebool,
                    create_date=customer.create_date,
                    last_update=customer.last_update,
                    active=customer.active
                )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.put("/customers/{customer_id}", response_model=Customer)
async def update_customer(customer_id: int, customer: Customer):
    """Update an existing customer"""
    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """UPDATE customer SET store_id = %s, first_name = %s, last_name = %s, email = %s, 
                       address_id = %s, activebool = %s, create_date = %s, last_update = %s, active = %s 
                       WHERE customer_id = %s""",
                    (customer.store_id, customer.first_name, customer.last_name, customer.email,
                     customer.address_id, customer.activebool, customer.create_date, customer.last_update, 
                     customer.active, customer_id)
                )
                if cur.rowcount == 0:
                    raise HTTPException(status_code=404, detail="Customer not found")
                conn.commit()
                
                return Customer(
                    customer_id=customer_id,
                    store_id=customer.store_id,
                    first_name=customer.first_name,
                    last_name=customer.last_name,
                    email=customer.email,
                    address_id=customer.address_id,
                    activebool=customer.activebool,
                    create_date=customer.create_date,
                    last_update=customer.last_update,
                    active=customer.active
                )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.delete("/customers/{customer_id}")
async def delete_customer(customer_id: int):
    """Delete a customer"""
    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM customer WHERE customer_id = %s", (customer_id,))
                if cur.rowcount == 0:
                    raise HTTPException(status_code=404, detail="Customer not found")
                conn.commit()
                return {"status": 200, "message": "Customer deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")