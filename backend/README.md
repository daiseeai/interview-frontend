# Movie Rental API Backend

A FastAPI-based backend for managing a movie rental database with PostgreSQL.

## Features

- **FastAPI** with automatic OpenAPI documentation
- **PostgreSQL** database with movie rental schema
- **Client Authentication** using client ID and secret
- **CRUD Operations** for customers, rentals, and payments
- **Read-only endpoints** for reference data
- **Database views** for reporting
- **Docker** containerization

## Quick Start with Docker

### Development Environment

1. **Start the services:**
   ```bash
   docker-compose up -d
   ```

2. **Check the API:**
   ```bash
   curl http://localhost:8000/health
   ```

3. **View API documentation:**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Production Environment

1. **Set environment variables:**
   ```bash
   export POSTGRES_PASSWORD=your_secure_password
   export POSTGRES_USER=your_db_user
   export POSTGRES_DB=your_db_name
   ```

2. **Start production services:**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

## Authentication

The API uses a single authorization token via Bearer authentication:

- **Authorization Token:** `A6484747478B6F8363FD436C79F89`

### Using Authorization Token

All API requests must include the authorization token in the Authorization header:

```bash
curl -X GET "http://localhost:8000/api/v1/customers" \
  -H "Authorization: Bearer A6484747478B6F8363FD436C79F89"
```

### Example Request with Response

**Request:**
```bash
curl -X GET 'http://localhost:8000/api/v1/customers?limit=5' \
  -H 'Authorization: Bearer A6484747478B6F8363FD436C79F89'
```

**Response:**
```json
[
  {
    "customer_id": 1,
    "store_id": 1,
    "first_name": "MARY",
    "last_name": "SMITH",
    "email": "MARY.SMITH@sakilacustomer.org",
    "address_id": 5,
    "activebool": true,
    "create_date": "2017-02-14",
    "last_update": "2017-02-15T06:57:20Z",
    "active": 1
  },
  {
    "customer_id": 2,
    "store_id": 1,
    "first_name": "PATRICIA",
    "last_name": "JOHNSON",
    "email": "PATRICIA.JOHNSON@sakilacustomer.org",
    "address_id": 6,
    "activebool": true,
    "create_date": "2017-02-14",
    "last_update": "2017-02-15T06:57:20Z",
    "active": 1
  },
  {
    "customer_id": 3,
    "store_id": 1,
    "first_name": "LINDA",
    "last_name": "WILLIAMS",
    "email": "LINDA.WILLIAMS@sakilacustomer.org",
    "address_id": 7,
    "activebool": true,
    "create_date": "2017-02-14",
    "last_update": "2017-02-15T06:57:20Z",
    "active": 1
  },
  {
    "customer_id": 4,
    "store_id": 2,
    "first_name": "BARBARA",
    "last_name": "JONES",
    "email": "BARBARA.JONES@sakilacustomer.org",
    "address_id": 8,
    "activebool": true,
    "create_date": "2017-02-14",
    "last_update": "2017-02-15T06:57:20Z",
    "active": 1
  },
  {
    "customer_id": 5,
    "store_id": 1,
    "first_name": "ELIZABETH",
    "last_name": "BROWN",
    "email": "ELIZABETH.BROWN@sakilacustomer.org",
    "address_id": 9,
    "activebool": true,
    "create_date": "2017-02-14",
    "last_update": "2017-02-15T06:57:20Z",
    "active": 1
  }
]
```

### Verifying Token

```bash
curl -X POST "http://localhost:8000/api/v1/auth/verify" \
  -H "Content-Type: application/json" \
  -d '{
    "token": "A6484747478B6F8363FD436C79F89"
  }'
```

### Checking Authentication Status

```bash
curl -X GET "http://localhost:8000/api/v1/auth/status" \
  -H "Authorization: Bearer A6484747478B6F8363FD436C79F89"
```

## API Endpoints

### Core CRUD Operations
- **Customers:** `/api/v1/customers`
- **Rentals:** `/api/v1/rentals`
- **Payments:** `/api/v1/payments`
- **Films:** `/api/v1/films`
- **Actors:** `/api/v1/actors`

### Reference Data (Read-only)
- **Categories:** `/api/v1/categories`
- **Languages:** `/api/v1/languages`
- **Addresses:** `/api/v1/addresses`
- **Cities:** `/api/v1/cities`
- **Countries:** `/api/v1/countries`
- **Stores:** `/api/v1/stores`
- **Staff:** `/api/v1/staff`
- **Inventory:** `/api/v1/inventory`

### Database Views
- **Customer List:** `/api/v1/views/customer-list`
- **Film List:** `/api/v1/views/film-list`
- **Sales by Category:** `/api/v1/views/sales-by-film-category`
- **Sales by Store:** `/api/v1/views/sales-by-store`
- **Staff List:** `/api/v1/views/staff-list`

## Development

### Local Development (without Docker)

1. **Install dependencies:**
   ```bash
   pip install poetry
   poetry install
   ```

2. **Set up PostgreSQL database:**
   - Create database: `movie_rental`
   - Run schema: `data/archive (1)/1. pagila-schema.sql`
   - Run data: `data/archive (1)/2. pagila-insert-data.sql`

3. **Run the application:**
   ```bash
   uvicorn main:app --reload
   ```

### Building the Docker Image

```bash
docker build -t movie-rental-api .
```

### Running Tests

```bash
# Run tests (when implemented)
pytest
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `POSTGRES_DB` | Database name | `movie_rental` |
| `POSTGRES_USER` | Database user | `postgres` |
| `POSTGRES_PASSWORD` | Database password | Required |
| `POSTGRES_PORT` | Database port | `5432` |
| `API_PORT` | API port | `8000` |
| `API_HOST` | API host | `0.0.0.0` |

## Health Checks

- **Application:** `GET /health`
- **Database:** Built into Docker Compose health checks

## Security

- Client ID/Secret authentication
- Non-root user in Docker container
- Parameterized SQL queries
- Input validation with Pydantic

## Monitoring

The application includes health checks and can be monitored through:
- Docker health checks
- FastAPI health endpoint
- Database connection status
