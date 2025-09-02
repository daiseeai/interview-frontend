
import psycopg
import os
from contextlib import contextmanager
from typing import Generator, Optional

# Connection pooling is not available in all psycopg versions
# We'll use simple connections for now
POOL_AVAILABLE = False

def get_database_url() -> str:
    """Get database URL from environment variables or use default"""
    return os.getenv(
        "DATABASE_URL", 
        "postgresql://postgres:postgres@localhost:5432/movie_rental"
    )

@contextmanager
def db_connection() -> Generator[psycopg.Connection, None, None]:
    """
    Context manager for database connections using psycopg3.
    
    Usage:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM table")
                result = cur.fetchall()
    """
    conn = None
    try:
        # Create connection
        conn = psycopg.connect(get_database_url())
        yield conn
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()

def get_db_connection() -> psycopg.Connection:
    """
    Get a database connection (without context manager).
    Caller is responsible for closing the connection.
    
    Usage:
        conn = get_db_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM table")
                result = cur.fetchall()
        finally:
            conn.close()
    """
    return psycopg.connect(get_database_url())

# Connection pool for better performance (if available)
_connection_pool = None

def get_connection_pool():
    """Get or create a connection pool (if available)"""
    global _connection_pool
    if not POOL_AVAILABLE:
        raise ImportError("Connection pooling not available. Install psycopg[binary] with pool support.")
    
    if _connection_pool is None:
        _connection_pool = psycopg.pool.ConnectionPool(
            get_database_url(),
            min_size=1,
            max_size=10,
            kwargs={"autocommit": False}
        )
    return _connection_pool

@contextmanager
def db_connection_pool() -> Generator[psycopg.Connection, None, None]:
    """
    Context manager for database connections using connection pool.
    Better for production use with multiple concurrent requests.
    Falls back to regular connections if pooling is not available.
    
    Usage:
        with db_connection_pool() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM table")
                result = cur.fetchall()
    """
    if POOL_AVAILABLE:
        pool = get_connection_pool()
        conn = None
        try:
            conn = pool.getconn()
            yield conn
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                pool.putconn(conn)
    else:
        # Fall back to regular connection if pool is not available
        with db_connection() as conn:
            yield conn

def close_connection_pool():
    """Close the connection pool (call on application shutdown)"""
    global _connection_pool
    if _connection_pool and POOL_AVAILABLE:
        _connection_pool.close()
        _connection_pool = None