def test_create_customer(client, admin_token):
    response = client.post("/api/v1/customers/", json={
        "name": "shop customer",
        "email": "shopcustomer@gmail.com",
        "phone": "08012345678",
        "address": "Lagos, Nigeria"
    }, headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    assert response.json()["name"] =="shop customer"
    assert response.json()["email"] == "shopcustomer@gmail.com"

def test_create_duplicate_customer(client, admin_token):
    client.post("/api/v1/customers/", json={
        "name": "Duplicate Customer",
        "email": "duplicate_customer@test.com",
        "phone": "08012345678",
        "address": "Lagos, Nigeria"
    }, headers={"Authorization": f"Bearer {admin_token}"})
    response = client.post("/api/v1/customers/", json={
        "name": "Duplicate Customer",
        "email": "duplicate_customer@test.com",
        "phone": "08012345678",
        "address": "Lagos, Nigeria"
    }, headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 400

def test_get_all_customers(client, admin_token):
    response = client.get("/api/v1/customers/",
        headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)

def test_get_single_customer(client, admin_token):
    create = client.post("/api/v1/customers/", json={
        "name": "Single Customer",
        "email": "singlecustomer@test.com",
        "phone": "08012345678",
        "address": "Lagos, Nigeria"
    }, headers={"Authorization": f"Bearer {admin_token}"})
    customer_id = create.json()["id"]
    response = client.get(f"/api/v1/customers/{customer_id}",
        headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    assert response.json()["name"] == "Single Customer"

def test_get_customer_not_found(client, admin_token):
    response = client.get("/api/v1/customers/99999",
        headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 404

def test_update_customer(client, admin_token):
    create = client.post("/api/v1/customers/", json={
        "name": "Update Customer",
        "email": "updatecustomer@test.com",
        "phone": "08012345678",
        "address": "Lagos, Nigeria"
    }, headers={"Authorization": f"Bearer {admin_token}"})
    customer_id = create.json()["id"]
    response = client.put(f"/api/v1/customers/{customer_id}", json={
        "name": "Updated Name"
    }, headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Name"

def test_delete_customer(client, admin_token):
    create = client.post("/api/v1/customers/", json={
        "name": "Delete Customer",
        "email": "deletecustomer@test.com",
        "phone": "08012345678",
        "address": "Lagos, Nigeria"
    }, headers={"Authorization": f"Bearer {admin_token}"})
    customer_id = create.json()["id"]
    response = client.delete(f"/api/v1/customers/{customer_id}",
        headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    assert response.json()["message"] == "Customer deleted successfully"

def test_search_customers(client, admin_token):
    client.post("/api/v1/customers/", json={
        "name": "Search Customer",
        "email": "searchcustomer@test.com",
        "phone": "08012345678",
        "address": "Lagos, Nigeria"
    }, headers={"Authorization": f"Bearer {admin_token}"})
    response = client.get("/api/v1/customers/?search=Search",
        headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) > 0