def test_create_user_success(client):
    response = client.post(
        "/api/v1/users",
        json={"username": "testuser", "password": "secret123", "telegram_id": 12345}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["telegram_id"] == 12345
    assert "id" in data

def test_get_user_success(client):
    create_response = client.post(
        "/api/v1/users",
        json={"username": "get_user", "password": "secret123", "telegram_id": 111}
    )
    user_id = create_response.json()["external_id"]

    response = client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["external_id"] == user_id
    assert data["username"] == "get_user"

def test_create_user_duplicate_telegram_id(client):
    client.post(
        "/api/v1/users",
        json={"username": "user_one", "password": "secret123", "telegram_id": 999}
    )
    
    response = client.post(
        "/api/v1/users",
        json={"username": "user_two", "password": "secret123", "telegram_id": 999}
    )
    
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "User with this telegram_id already exists" # <-- Текст ошибки изменился