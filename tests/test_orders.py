def test_create_order(client, admin_token):
    
    product = client.post("/products/", json={
        "name": "Order Product",
        "description": "Test",
        "price": 5000,
        "stock": 10,
        "category": "Test",
        "low_stock_threshold": 2
    }, headers={"Authorization": f"Bearer {admin_token}"})
    product_id = product.json()["id"]

    
    customer = client.post("/customers/", json={
        "name": "Order Customer",
        "email": "ordercustomer@test.com",
        "phone": "08012345678",
        "address": "Lagos, Nigeria"
    }, headers={"Authorization": f"Bearer {admin_token}"})
    customer_id = customer.json()["id"]

    
    response = client.post("/orders/", json={
        "customer_id": customer_id,
        "items": [{"product_id": product_id, "quantity": 2}],
        "payment_status": "paid"
    }, headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    assert response.json()["total"] == 10000
    assert response.json()["payment_status"] == "paid"

def test_create_order_insufficient_stock(client, admin_token):
    
    product = client.post("/products/", json={
        "name": "Low Stock Product",
        "description": "Test",
        "price": 5000,
        "stock": 2,
        "category": "Test",
        "low_stock_threshold": 1
    }, headers={"Authorization": f"Bearer {admin_token}"})
    product_id = product.json()["id"]

    
    customer = client.post("/customers/", json={
        "name": "Stock Customer",
        "email": "stockcustomer@test.com",
        "phone": "08012345678",
        "address": "Lagos, Nigeria"
    }, headers={"Authorization": f"Bearer {admin_token}"})
    customer_id = customer.json()["id"]

    
    response = client.post("/orders/", json={
        "customer_id": customer_id,
        "items": [{"product_id": product_id, "quantity": 10}],
        "payment_status": "paid"
    }, headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 400

def test_get_all_orders(client, admin_token):
    response = client.get("/orders/",
        headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_single_order(client, admin_token):
    
    product = client.post("/products/", json={
        "name": "Single Order Product",
        "description": "Test",
        "price": 3000,
        "stock": 5,
        "category": "Test",
        "low_stock_threshold": 2
    }, headers={"Authorization": f"Bearer {admin_token}"})
    product_id = product.json()["id"]

    customer = client.post("/customers/", json={
        "name": "Single Order Customer",
        "email": "singleordercustomer@test.com",
        "phone": "08012345678",
        "address": "Lagos, Nigeria"
    }, headers={"Authorization": f"Bearer {admin_token}"})
    customer_id = customer.json()["id"]

    
    create = client.post("/orders/", json={
        "customer_id": customer_id,
        "items": [{"product_id": product_id, "quantity": 1}],
        "payment_status": "pending"
    }, headers={"Authorization": f"Bearer {admin_token}"})
    order_id = create.json()["id"]

    
    response = client.get(f"/orders/{order_id}",
        headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    assert response.json()["id"] == order_id

def test_update_order_status(client, admin_token):
    
    product = client.post("/products/", json={
        "name": "Update Order Product",
        "description": "Test",
        "price": 3000,
        "stock": 5,
        "category": "Test",
        "low_stock_threshold": 2
    }, headers={"Authorization": f"Bearer {admin_token}"})
    product_id = product.json()["id"]

    customer = client.post("/customers/", json={
        "name": "Update Order Customer",
        "email": "updateordercustomer@test.com",
        "phone": "08012345678",
        "address": "Lagos, Nigeria"
    }, headers={"Authorization": f"Bearer {admin_token}"})
    customer_id = customer.json()["id"]

    
    create = client.post("/orders/", json={
        "customer_id": customer_id,
        "items": [{"product_id": product_id, "quantity": 1}],
        "payment_status": "pending"
    }, headers={"Authorization": f"Bearer {admin_token}"})
    order_id = create.json()["id"]

    
    response = client.put(f"/orders/{order_id}", json={
        "payment_status": "paid",
        "order_status": "delivered"
    }, headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    assert response.json()["payment_status"] == "paid"
    assert response.json()["order_status"] == "delivered"