def test_register_admin(client):
    response = client.post("/api/v1/auth/register", json={
        "name": "John Admin",
        "email": "johnadmin@test.com",
        "password": "admin123",
        "role": "admin"
    })
    assert response.status_code == 200
    assert response.json()["email"] == "johnadmin@test.com"
    assert response.json()["role"] == "admin"

def test_register_customer(client):
    response = client.post("/api/v1/auth/register", json={
        "name": "John Customer",
        "email": "johncustomer@test.com",
        "password": "customer123"
    })
    assert response.status_code == 200
    assert response.json()["role"] == "customer"

def test_register_duplicate_email(client):
    client.post("/api/v1/auth/register", json={
        "name": "John Admin",
        "email": "duplicate@test.com",
        "password": "admin123"
    })
    response = client.post("/api/v1/auth/register", json={
        "name": "John Admin",
        "email": "duplicate@test.com",
        "password": "admin123"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_login_success(client):
    reg_resp = client.post("/api/v1/auth/register", json={
        "name": "Login Test",
        "email": "logintest@test.com",
        "password": "password123"
    })
    assert reg_resp.status_code == 200
    
    response = client.post("/api/v1/auth/login", json={
        "email": "logintest@test.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_wrong_password(client):
    client.post("/api/v1/auth/register", json={
        "name": "Wrong Pass",
        "email": "wrongpass@test.com",
        "password": "correct123"
    })
    
    response = client.post("/api/v1/auth/login", json={
        "email": "wrongpass@test.com",
        "password": "wrongpassword"
    })
    # Anti-enumeration: wrong password returns 401, not 400
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"

def test_login_user_not_found(client):
    response = client.post("/api/v1/auth/login", json={
        "email": "nobody@test.com",
        "password": "test123"
    })
    # Anti-enumeration: non-existent user returns 401 (same as wrong password)
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"