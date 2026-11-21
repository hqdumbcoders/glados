def test_login_success(client):
    client.post(
        "/api/v1/accounts",
        json={"username": "login_user", "password": "secret123"}
    )

    response = client.post(
        "/api/v1/auth/login",
        json={"username": "login_user", "password": "secret123"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password(client):
    client.post(
        "/api/v1/accounts",
        json={"username": "login_use_wrong", "password": "secret123"}
    )

    response = client.post(
        "/api/v1/auth/login",
        json={"username": "login_user_wrong", "password": "wrong_password"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"

def test_refresh_and_logout(client):
    client.post(
        "/api/v1/accounts",
        json={"username": "refresh_user_test", "password": "secret123"}
    )
    login_response = client.post(
        "/api/v1/auth/login",
        json={"username": "refresh_user_test", "password": "secret123"}
    )
    refresh_token = login_response.json()["refresh_token"]

    refresh_response = client.post(
        "api/v1/auth/refresh",
        json={"refresh_token": refresh_token}
    )
    assert refresh_response.status_code == 200
    assert "access_token" in refresh_response.json()

    logout_response = client.post(
        "api/v1/auth/logout",
        json={"refresh_token": refresh_token}
    )
    assert logout_response.status_code == 200

    bad_refresh_response = client.post(
        "api/v1/auth/refresh",
        json={"refresh_token": refresh_token}
    )
    assert bad_refresh_response.status_code == 401