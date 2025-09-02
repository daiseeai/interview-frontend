from fastapi import FastAPI
from src.routes import (
    actors, addresses, auth, categories, cities, countries, customers, 
    films, inventory, languages, payments, rentals, staff, stores, views
)
from src.middleware.auth import AuthMiddleware
from src.utils.database import close_connection_pool
from fastapi.openapi.utils import get_openapi

app = FastAPI(
    title="Movie Rental API",
    description="API for managing movie rental database with client authentication",
    version="1.0.0"
)

# Add authentication middleware
auth_middleware = AuthMiddleware()
app.middleware("http")(auth_middleware)

# Include all route modules
app.include_router(auth.router, prefix="/api/v1", tags=["authentication"])
app.include_router(actors.router, prefix="/api/v1", tags=["actors"])
app.include_router(addresses.router, prefix="/api/v1", tags=["addresses"])
app.include_router(categories.router, prefix="/api/v1", tags=["categories"])
app.include_router(cities.router, prefix="/api/v1", tags=["cities"])
app.include_router(countries.router, prefix="/api/v1", tags=["countries"])
app.include_router(customers.router, prefix="/api/v1", tags=["customers"])
app.include_router(films.router, prefix="/api/v1", tags=["films"])
app.include_router(inventory.router, prefix="/api/v1", tags=["inventory"])
app.include_router(languages.router, prefix="/api/v1", tags=["languages"])
app.include_router(payments.router, prefix="/api/v1", tags=["payments"])
app.include_router(rentals.router, prefix="/api/v1", tags=["rentals"])
app.include_router(staff.router, prefix="/api/v1", tags=["staff"])
app.include_router(stores.router, prefix="/api/v1", tags=["stores"])
app.include_router(views.router, prefix="/api/v1", tags=["views"])

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Custom API",
        version="2.0.0",
        description="This is a custom OpenAPI schema",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on application shutdown"""
    close_connection_pool()

@app.get("/health")
def read_root():
    return {"status": 200, "message": "Healthy"}

@app.get("/health/db")
def health_check_db():
    """Check database connectivity"""
    try:
        from src.utils.database import db_connection
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                result = cur.fetchone()
                if result:
                    return {"status": 200, "message": "Database connection healthy"}
    except Exception as e:
        return {"status": 500, "message": f"Database connection failed: {str(e)}"}