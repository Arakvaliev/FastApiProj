def test_create_vacancy(client, auth_headers, sample_position, sample_category):
    response = client.post(
        "/api/v1/vacancies/",
        json={
            "title": "Senior Developer",
            "description": "Looking for an experienced developer",
            "position_id": sample_position.id,
            "category_id": sample_category.id,
            "min_salary": 150000
        },
        headers=auth_headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Senior Developer"
    assert data["min_salary"] == 150000
    assert data["status"] == "open"
    assert data["position"]["id"] == sample_position.id
    assert data["category"]["id"] == sample_category.id

def test_get_vacancies_with_filters(client, auth_headers, sample_position, sample_category):
    client.post("/api/v1/vacancies/", json={
        "title": "Junior Developer",
        "description": "Entry level position",
        "position_id": sample_position.id,
        "category_id": sample_category.id,
        "min_salary": 80000
    }, headers=auth_headers)
    
    client.post("/api/v1/vacancies/", json={
        "title": "Senior Developer",
        "description": "Senior level position",
        "position_id": sample_position.id,
        "category_id": sample_category.id,
        "min_salary": 200000
    }, headers=auth_headers)
    
    response = client.get("/api/v1/vacancies/?min_salary=150000", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["min_salary"] >= 150000

    response = client.get(f"/api/v1/vacancies/?category_id={sample_category.id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    
    response = client.get("/api/v1/vacancies/?status=open", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

def test_update_vacancy(client, auth_headers, sample_position, sample_category):
    create_response = client.post("/api/v1/vacancies/", json={
        "title": "Developer",
        "description": "Test description",
        "position_id": sample_position.id,
        "category_id": sample_category.id,
        "min_salary": 100000
    }, headers=auth_headers)
    vacancy_id = create_response.json()["id"]
    
    update_response = client.put(
        f"/api/v1/vacancies/{vacancy_id}",
        json={"title": "Updated Developer", "min_salary": 120000},
        headers=auth_headers
    )
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["title"] == "Updated Developer"
    assert data["min_salary"] == 120000

def test_delete_vacancy(client, auth_headers, sample_position, sample_category):
    create_response = client.post("/api/v1/vacancies/", json={
        "title": "Developer",
        "description": "Test description",
        "position_id": sample_position.id,
        "category_id": sample_category.id,
        "min_salary": 100000
    }, headers=auth_headers)
    vacancy_id = create_response.json()["id"]
    
    delete_response = client.delete(f"/api/v1/vacancies/{vacancy_id}", headers=auth_headers)
    assert delete_response.status_code == 200
    
    get_response = client.get(f"/api/v1/vacancies/{vacancy_id}", headers=auth_headers)
    assert get_response.status_code == 404

def test_get_vacancy_by_id(client, auth_headers, sample_position, sample_category):
    create_response = client.post("/api/v1/vacancies/", json={
        "title": "Developer",
        "description": "Test",
        "position_id": sample_position.id,
        "category_id": sample_category.id,
        "min_salary": 100000
    }, headers=auth_headers)
    vacancy_id = create_response.json()["id"]
    
    response = client.get(f"/api/v1/vacancies/{vacancy_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Developer"
    assert response.json()["position"]["name"] == "Software Developer"

def test_get_nonexistent_vacancy(client, auth_headers):
    response = client.get("/api/v1/vacancies/999", headers=auth_headers)
    assert response.status_code == 404

def test_update_other_hr_vacancy(client, auth_headers, sample_position, sample_category):
    client.post("/api/v1/auth/register", json={
        "first_name": "Other",
        "last_name": "HR",
        "login": "otherhr",
        "password": "password123"
    })
    other_login = client.post("/api/v1/auth/login", json={
        "login": "otherhr",
        "password": "password123"
    })
    other_token = other_login.json()["access_token"]
    other_headers = {"Authorization": f"Bearer {other_token}"}
    
    create_response = client.post("/api/v1/vacancies/", json={
        "title": "Other HR Vacancy",
        "description": "Test",
        "position_id": sample_position.id,
        "category_id": sample_category.id,
        "min_salary": 100000
    }, headers=other_headers)
    vacancy_id = create_response.json()["id"]
    
    response = client.put(
        f"/api/v1/vacancies/{vacancy_id}",
        json={"title": "Hacked"},
        headers=auth_headers
    )
    assert response.status_code == 403

def test_create_position(client, auth_headers):
    response = client.post(
        "/api/v1/vacancies/positions",
        json={"name": "Team Lead"},
        headers=auth_headers
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Team Lead"

def test_create_duplicate_position(client, auth_headers):
    client.post("/api/v1/vacancies/positions", json={"name": "Designer"}, headers=auth_headers)
    response = client.post("/api/v1/vacancies/positions", json={"name": "Designer"}, headers=auth_headers)
    assert response.status_code == 400

def test_delete_position_with_vacancies(client, auth_headers, sample_position, sample_category):
    client.post("/api/v1/vacancies/", json={
        "title": "Dev",
        "description": "Test",
        "position_id": sample_position.id,
        "category_id": sample_category.id,
        "min_salary": 100000
    }, headers=auth_headers)
    
    response = client.delete(f"/api/v1/vacancies/positions/{sample_position.id}", headers=auth_headers)
    assert response.status_code == 400