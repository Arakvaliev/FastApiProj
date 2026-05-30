def test_create_resume(client, auth_headers, sample_category):
    response = client.post(
        "/api/v1/resumes/",
        json={
            "first_name": "Jane",
            "last_name": "Smith",
            "gender": "female",
            "age": 28,
            "phone": "+79161234567",
            "email": "jane.smith@example.com",
            "experience_years": 5,
            "higher_education": True,
            "category_id": sample_category.id,
            "status": "new"
        },
        headers=auth_headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["first_name"] == "Jane"
    assert data["last_name"] == "Smith"
    assert data["experience_years"] == 5
    assert data["higher_education"] == True
    assert data["category"]["id"] == sample_category.id

def test_get_resumes_with_filters(client, auth_headers, sample_category):
    client.post("/api/v1/resumes/", json={
        "first_name": "Junior",
        "last_name": "Dev",
        "gender": "male",
        "age": 23,
        "phone": "+79161111111",
        "email": "junior@example.com",
        "experience_years": 1,
        "higher_education": False,
        "category_id": sample_category.id,
        "status": "new"
    }, headers=auth_headers)
    
    client.post("/api/v1/resumes/", json={
        "first_name": "Senior",
        "last_name": "Dev",
        "gender": "male",
        "age": 35,
        "phone": "+79162222222",
        "email": "senior@example.com",
        "experience_years": 10,
        "higher_education": True,
        "category_id": sample_category.id,
        "status": "interviewed"
    }, headers=auth_headers)
    
    response = client.get("/api/v1/resumes/?min_experience=5", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    
    response = client.get("/api/v1/resumes/?higher_education=true", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    
    response = client.get("/api/v1/resumes/?status=new", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1

def test_update_resume(client, auth_headers, sample_category):
    create_response = client.post("/api/v1/resumes/", json={
        "first_name": "Test",
        "last_name": "User",
        "gender": "male",
        "age": 30,
        "phone": "+79163333333",
        "email": "test@example.com",
        "experience_years": 3,
        "higher_education": True,
        "category_id": sample_category.id,
        "status": "new"
    }, headers=auth_headers)
    resume_id = create_response.json()["id"]
    
    update_response = client.put(
        f"/api/v1/resumes/{resume_id}",
        json={"status": "in_progress", "experience_years": 4},
        headers=auth_headers
    )
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["status"] == "in_progress"
    assert data["experience_years"] == 4

def test_delete_resume(client, auth_headers, sample_category):
    create_response = client.post("/api/v1/resumes/", json={
        "first_name": "Test",
        "last_name": "User",
        "gender": "male",
        "age": 30,
        "phone": "+79164444444",
        "email": "test2@example.com",
        "experience_years": 2,
        "higher_education": False,
        "category_id": sample_category.id,
        "status": "new"
    }, headers=auth_headers)
    resume_id = create_response.json()["id"]
    
    delete_response = client.delete(f"/api/v1/resumes/{resume_id}", headers=auth_headers)
    assert delete_response.status_code == 200
    
    get_response = client.get(f"/api/v1/resumes/{resume_id}", headers=auth_headers)
    assert get_response.status_code == 404

def test_create_resume_nonexistent_category(client, auth_headers):
    response = client.post("/api/v1/resumes/", json={
        "first_name": "Test",
        "last_name": "User",
        "gender": "male",
        "age": 30,
        "phone": "+79161234567",
        "email": "test@example.com",
        "experience_years": 5,
        "higher_education": True,
        "category_id": 999,
        "status": "new"
    }, headers=auth_headers)
    assert response.status_code == 404

def test_get_nonexistent_resume(client, auth_headers):
    response = client.get("/api/v1/resumes/999", headers=auth_headers)
    assert response.status_code == 404

def test_resume_validation(client, auth_headers, sample_category):
    response = client.post("/api/v1/resumes/", json={
        "first_name": "Test",
        "last_name": "User",
        "gender": "male",
        "age": 30,
        "phone": "+79161234567",
        "email": "invalid-email",
        "experience_years": 5,
        "higher_education": True,
        "category_id": sample_category.id,
        "status": "new"
    }, headers=auth_headers)
    assert response.status_code == 422
    
    response = client.post("/api/v1/resumes/", json={
        "first_name": "Test",
        "last_name": "User",
        "gender": "male",
        "age": 30,
        "phone": "+79161234567",
        "email": "valid@example.com",
        "experience_years": 5,
        "higher_education": True,
        "category_id": sample_category.id,
        "status": "invalid_status"
    }, headers=auth_headers)
    assert response.status_code == 422

def test_filter_by_vacancy_id(client, auth_headers, sample_position, sample_category):
    vacancy_response = client.post("/api/v1/vacancies/", json={
        "title": "Python Dev",
        "description": "Test",
        "position_id": sample_position.id,
        "category_id": sample_category.id,
        "min_salary": 150000
    }, headers=auth_headers)
    vacancy_id = vacancy_response.json()["id"]
    
    client.post("/api/v1/resumes/", json={
        "first_name": "Python",
        "last_name": "Developer",
        "gender": "male",
        "age": 25,
        "phone": "+79161234567",
        "email": "python@example.com",
        "experience_years": 3,
        "higher_education": True,
        "category_id": sample_category.id,
        "vacancy_id": vacancy_id,
        "status": "new"
    }, headers=auth_headers)
    
    response = client.get(f"/api/v1/resumes/?vacancy_id={vacancy_id}", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 1