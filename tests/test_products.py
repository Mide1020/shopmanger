def test_create_product(client, admin_token):
    response = client.post("/api/v1/products/", json={
        "name": "Test Product",
        "description": "A test product",
        "price": 5000,
        "stock": 10,
        "category": "Test",
        "low_stock_threshold": 3
    }, headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    assert response.json()["name"] == "Test Product"
    assert response.json()["price"] == 5000

def test_create_product_unauthorized(client, customer_token):
    response = client.post("/api/v1/products/", json={
        "name": "Test Product",
        "description": "A test product",
        "price": 5000,
        "stock": 10,
        "category": "Test",
        "low_stock_threshold": 3
    }, headers={"Authorization": f"Bearer {customer_token}"})
    assert response.status_code == 403

def test_get_all_products(client):
    response = client.get("/api/v1/products/")
    assert response.status_code == 200
    data = response.json()
    # Response is now a paginated envelope, not a bare list
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert "limit" in data
    assert "pages" in data
    assert isinstance(data["items"], list)

def test_get_single_product(client, admin_token):
    
    create = client.post("/api/v1/products/", json={
        "name": "Single Product",
        "description": "Test",
        "price": 3000,
        "stock": 5,
        "category": "Test",
        "low_stock_threshold": 2
    }, headers={"Authorization": f"Bearer {admin_token}"})
    product_id = create.json()["id"]

    
    response = client.get(f"/api/v1/products/{product_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Single Product"

def test_get_product_not_found(client):
    response = client.get("/api/v1/products/99999")
    assert response.status_code == 404

def test_update_product(client, admin_token):
    
    create = client.post("/api/v1/products/", json={
        "name": "Update Product",
        "description": "Test",
        "price": 3000,
        "stock": 5,
        "category": "Test",
        "low_stock_threshold": 2
    }, headers={"Authorization": f"Bearer {admin_token}"})
    product_id = create.json()["id"]

    
    response = client.put(f"/api/v1/products/{product_id}", json={
        "price": 4000
    }, headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    assert response.json()["price"] == 4000

def test_delete_product(client, admin_token):
    
    create = client.post("/api/v1/products/", json={
        "name": "Delete Product",
        "description": "Test",
        "price": 3000,
        "stock": 5,
        "category": "Test",
        "low_stock_threshold": 2
    }, headers={"Authorization": f"Bearer {admin_token}"})
    product_id = create.json()["id"]

    
    response = client.delete(f"/api/v1/products/{product_id}",
        headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    assert response.json()["message"] == "Product deleted successfully"