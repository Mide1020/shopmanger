import pytest
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

os.environ["TESTING"] = "1"

from app.main import app
from app.database import Base, get_db
from app.utils.rate_limit import limiter

# Disable rate limiting for the test suite
limiter.enabled = False

TEST_DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://postgres:1234@localhost:5432/shopmanager_test"
)


engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def clean_db():
    # Drop and recreate all tables before each test
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield

@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture
def admin_token(client):
    client.post("/api/v1/auth/register", json={
        "name": "Test Admin",
        "email": "testadmin@shopmanager.com",
        "password": "admin123",
        "role": "admin"
    })
    
    response = client.post("/api/v1/auth/login", json={
        "email": "testadmin@shopmanager.com",
        "password": "admin123"
    })
    return response.json()["access_token"]

@pytest.fixture
def customer_token(client):
    client.post("/api/v1/auth/register", json={
        "name": "Test Customer",
        "email": "testcustomer@shopmanager.com",
        "password": "customer123",
        "role": "customer"
    })
    
    response = client.post("/api/v1/auth/login", json={
        "email": "testcustomer@shopmanager.com",
        "password": "customer123"
    })
    return response.json()["access_token"]