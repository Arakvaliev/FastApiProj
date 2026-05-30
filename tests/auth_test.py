def test_register_user(client):
    response = client.post("/api/v1/auth/register", json={
        "first_name": "John",
        "last_name": "Doe",
        "login": "johndoe",
        "password": "password123"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["first_name"] == "John"
    assert data["last_name"] == "Doe"
    assert data["login"] == "johndoe"
    assert "id" in data

def test_register_duplicate_login(client):
    client.post("/api/v1/auth/register", json={
        "first_name": "John",
        "last_name": "Doe",
        "login": "johndoe",
        "password": "password123"
    })
    
    response = client.post("/api/v1/auth/register", json={
        "first_name": "Jane",
        "last_name": "Doe",
        "login": "johndoe",
        "password": "password456"
    })
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]

def test_register_short_password(client):
    response = client.post("/api/v1/auth/register", json={
        "first_name": "John",
        "last_name": "Doe",
        "login": "johndoe",
        "password": "short"
    })
    assert response.status_code == 422

def test_login(client, db_session):
    client.post("/api/v1/auth/register", json={
        "first_name": "John",
        "last_name": "Doe",
        "login": "johndoe",
        "password": "password123"
    })
    
    response = client.post("/api/v1/auth/login", json={
        "login": "johndoe",
        "password": "password123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials(client):
    response = client.post("/api/v1/auth/login", json={
        "login": "nonexistent",
        "password": "wrongpassword"
    })
    assert response.status_code == 401

def test_change_password(client, auth_headers):
    response = client.post(
        "/api/v1/auth/change-password",
        json={
            "old_password": "testpassword123",
            "new_password": "newpassword123"
        },
        headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Password changed successfully"

def test_refresh_token(client, auth_headers):
    response = client.post("/api/v1/auth/login", json={
        "login": "testuser",
        "password": "testpassword123"
    })
    refresh_token = response.json()["refresh_token"]
    
    refresh_response = client.post("/api/v1/auth/refresh", json={
        "refresh_token": refresh_token
    })
    assert refresh_response.status_code == 200
    assert "access_token" in refresh_response.json()

def test_get_current_user(client, auth_headers):
    response = client.get("/api/v1/auth/me", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["login"] == "testuser"

def test_change_password_wrong_old(client, auth_headers):
    response = client.post(
        "/api/v1/auth/change-password",
        json={
            "old_password": "wrongpassword",
            "new_password": "newpassword123"
        },
        headers=auth_headers
    )
    assert response.status_code == 400
