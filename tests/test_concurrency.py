"""
Concurrency test: verifies that simultaneous orders cannot drive stock below zero.

We create a product with stock=5, then fire 10 concurrent threads each trying to
order 1 unit. At most 5 should succeed; stock must never go negative.
"""
import threading
import pytest
from fastapi.testclient import TestClient


def test_concurrent_orders_no_negative_stock(client, admin_token):
    # --- setup: product with stock=5 ---
    product_resp = client.post("/api/v1/products/", json={
        "name": "Concurrency Test Product",
        "description": "Race condition test",
        "price": 100,
        "stock": 5,
        "category": "Test",
        "low_stock_threshold": 1
    }, headers={"Authorization": f"Bearer {admin_token}"})
    assert product_resp.status_code == 200
    product_id = product_resp.json()["id"]

    # --- setup: one customer ---
    customer_resp = client.post("/api/v1/customers/", json={
        "name": "Concurrent Customer",
        "email": "concurrent@test.com",
        "phone": "08099999999",
        "address": "Lagos, Nigeria"
    }, headers={"Authorization": f"Bearer {admin_token}"})
    assert customer_resp.status_code == 200
    customer_id = customer_resp.json()["id"]

    # --- fire 10 threads, each ordering 1 unit ---
    results = []
    lock = threading.Lock()

    def place_order():
        resp = client.post("/api/v1/orders/", json={
            "customer_id": customer_id,
            "items": [{"product_id": product_id, "quantity": 1}],
            "payment_status": "paid"
        }, headers={"Authorization": f"Bearer {admin_token}"})
        with lock:
            results.append(resp.status_code)

    threads = [threading.Thread(target=place_order) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    successes = results.count(200)
    failures = [r for r in results if r != 200]

    # At most 5 orders should succeed (stock=5)
    assert successes <= 5, f"Too many orders succeeded: {successes}"
    # At least some should have been rejected
    assert len(failures) >= 5, f"Expected at least 5 rejections, got: {failures}"

    # Verify stock is never negative via product fetch
    product_detail = client.get(f"/api/v1/products/{product_id}")
    assert product_detail.status_code == 200
    remaining_stock = product_detail.json()["stock"]
    assert remaining_stock >= 0, f"Stock went negative: {remaining_stock}"
