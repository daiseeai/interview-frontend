from fastapi import APIRouter, HTTPException
from typing import List
from src.schemas.actor import Actor
from src.utils.database import db_connection

router = APIRouter()

@router.get("/actors", response_model=List[Actor])
async def get_actors(limit: int = 100, offset: int = 0):
    """Get all actors with pagination"""
    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT actor_id, first_name, last_name, last_update FROM actor ORDER BY actor_id LIMIT %s OFFSET %s",
                    (limit, offset)
                )
                actors = []
                for row in cur.fetchall():
                    actors.append(Actor(
                        actor_id=row[0],
                        first_name=row[1],
                        last_name=row[2],
                        last_update=row[3]
                    ))
                return actors
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/actors/{actor_id}", response_model=Actor)
async def get_actor(actor_id: int):
    """Get a specific actor by ID"""
    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT actor_id, first_name, last_name, last_update FROM actor WHERE actor_id = %s",
                    (actor_id,)
                )
                row = cur.fetchone()
                if not row:
                    raise HTTPException(status_code=404, detail="Actor not found")
                
                return Actor(
                    actor_id=row[0],
                    first_name=row[1],
                    last_name=row[2],
                    last_update=row[3]
                )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.post("/actors", response_model=Actor)
async def create_actor(actor: Actor):
    """Create a new actor"""
    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO actor (first_name, last_name, last_update) VALUES (%s, %s, %s) RETURNING actor_id",
                    (actor.first_name, actor.last_name, actor.last_update)
                )
                actor_id = cur.fetchone()[0]
                conn.commit()
                
                return Actor(
                    actor_id=actor_id,
                    first_name=actor.first_name,
                    last_name=actor.last_name,
                    last_update=actor.last_update
                )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.put("/actors/{actor_id}", response_model=Actor)
async def update_actor(actor_id: int, actor: Actor):
    """Update an existing actor"""
    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE actor SET first_name = %s, last_name = %s, last_update = %s WHERE actor_id = %s",
                    (actor.first_name, actor.last_name, actor.last_update, actor_id)
                )
                if cur.rowcount == 0:
                    raise HTTPException(status_code=404, detail="Actor not found")
                conn.commit()
                
                return Actor(
                    actor_id=actor_id,
                    first_name=actor.first_name,
                    last_name=actor.last_name,
                    last_update=actor.last_update
                )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.delete("/actors/{actor_id}")
async def delete_actor(actor_id: int):
    """Delete an actor"""
    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM actor WHERE actor_id = %s", (actor_id,))
                if cur.rowcount == 0:
                    raise HTTPException(status_code=404, detail="Actor not found")
                conn.commit()
                return {"status": 200, "message": "Actor deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
