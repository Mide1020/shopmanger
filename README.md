#ShopManager API

ShopManager is a high performance, self managed e-commerce backend built with a modern Python stack. It is designed to handle the entire lifecycle of a retail business from catalog and inventory management, to order processing and invoicing.

#Tech Stack

*   **Framework:** [FastAPI](https://fastapi.tiangolo.com/) (High-performance web framework)
*   **Database ORM:** [SQLAlchemy](https://www.sqlalchemy.org/)
*   **Migrations:** [Alembic](https://alembic.sqlalchemy.org/en/latest/)
*   **Rate Limiting:** [SlowAPI](https://slowapi.readthedocs.io/en/latest/)
*   **Testing:** [Pytest](https://docs.pytest.org/en/7.4.x/)

## Key Features

*   **Authentication & Roles:** JWT-based user authentication separating internal admins from everyday customers.
*   **Products & Inventory:** Manage your catalog with full CRUD operations and dedicated dynamic stock tracking.
*   **Orders & Invoices:** Process customer orders safely using row-level locking to prevent race conditions, alongside an automated invoicing system.
*   **Business Analytics:** Dedicated dashboard endpoints to track sales, active users, and inventory status.
*   **Rate Limiting Built-in:** Endpoints protected against abuse and DDoS attacks.
*   **Robust Testing:** Powered by Pytest for continuous confidence in system health.

## Getting Started

### 1. Requirements

Make sure you have Python 3.10+ installed and a running PostgreSQL database.

### 2. Installation

Clone the repository and set up a virtual environment:

```bash
# Create and activate a virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install dependencies (ensure a requirements.txt exists or install manually)
pip install fastapi uvicorn sqlalchemy alembic psycopg2-binary slowapi pytest httpx python-jose passlib bcrypt
```

### 3. Environment Variables

Create a `.env` file in the root directory and ensure you configure your connection strings. 

### 4. Database Migrations

Run Alembic to create your database tables:

```bash
alembic upgrade head
```

### 5. Running the Application

Start the local development server with Uvicorn:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`. You can interact with the dynamic Swagger documentation at `http://localhost:8000/docs`.

## Testing

The codebase includes an extensive suite of automated tests. You can run them using:

```bash
pytest
```
*(Note: Tests are configured to automatically ignore API rate-limiting so they run swiftly without 429 errors).*
