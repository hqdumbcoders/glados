def test_create_account_success(client):
    response = client.post(
        "/api/v1/accounts",
        json={"username": "testuser", "telegram_id": 12345}
    )

    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["telegram_id"] == 12345
    assert "id" in data

def test_get_account_success(client):
    create_response = client.post(
        "/api/v1/accounts",
        json={"username": "get_user", "telegram_id": 111}
    )

    account_id = create_response.json()["id"]

    response = client.get(f"/api/v1/accounts/{account_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == account_id
    assert data["username"] == "get_user"

def test_create_account_duplicate_telegram_id(client):
    client.post(
        "/api/v1/accounts",
        json={"username": "user_one", "telegram_id": 999}
    )

    response = client.post(
        "/api/v1/accounts",
        json={"username": "user_two", "telegram_id": 999}
    )

    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Account with this telegram_id already exists"