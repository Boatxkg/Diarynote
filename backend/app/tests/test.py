import pytest
from models import User, Note
from flask_jwt_extended import create_access_token

# ---------- Fixture ----------
@pytest.fixture
def test_user_data():
    return {
        "username": "testuser_auth",
        "password": "testpass123"
    }

@pytest.fixture
def auth_header(test_user_data, client):
    # Register
    client.post("/api/register", json=test_user_data)

    # Login
    response = client.post("/api/login", json=test_user_data)
    token = response.get_json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    yield headers


@pytest.fixture(autouse=True)
def cleanup():
    yield
    # Cleanup ทั้งหมด (กันพลาด)
    User.objects.delete()
    Note.objects.delete()

# ---------- Auth Tests ----------
def test_register_success(client, test_user_data):
    response = client.post("/api/register", json=test_user_data)
    assert response.status_code == 200
    assert response.get_json()["msg"] == "User registered successfully"

def test_register_duplicate(client, test_user_data):
    client.post("/api/register", json=test_user_data)
    response = client.post("/api/register", json=test_user_data)
    assert response.status_code == 400
    assert response.get_json()["msg"] == "Username already exists"

def test_login_success(client, test_user_data):
    client.post("/api/register", json=test_user_data)
    response = client.post("/api/login", json=test_user_data)
    assert response.status_code == 200
    assert "access_token" in response.get_json()

def test_login_wrong_password(client, test_user_data):
    client.post("/api/register", json=test_user_data)
    response = client.post("/api/login", json={
        "username": test_user_data["username"],
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    assert response.get_json()["msg"] == "Invalid credentials"

def test_logout(client, test_user_data):
    # Register และ Login เพื่อให้ได้ token
    client.post("/api/register", json=test_user_data)
    res = client.post("/api/login", json=test_user_data)
    token = res.get_json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # เรียก /logout
    res = client.post("/api/logout", headers=headers)
    assert res.status_code == 200
    assert res.get_json()["msg"] == "Logged out"

    # ตรวจสอบว่า token ถูกเพิ่มใน blacklist
    from routes.auth import blacklist
    from flask_jwt_extended import decode_token
    jti = decode_token(token)["jti"]
    assert jti in blacklist
    
def test_show_users(client, test_user_data):
    client.post("/api/register", json=test_user_data)
    response = client.get("/api/showuser")
    assert response.status_code == 200
    users = response.get_json()
    assert any(u["username"] == test_user_data["username"] for u in users)

# ---------- Notes Tests ----------
def test_create_note(client, auth_header):
    response = client.post("/api/notes", json={
        "title": "Test Note",
        "content": "This is a test note."
    }, headers=auth_header)
    assert response.status_code == 200
    assert response.get_json()["msg"] == "Note created!"

def test_get_notes(client, auth_header):
    client.post("/api/notes", json={
        "title": "My Note",
        "content": "Content"
    }, headers=auth_header)

    response = client.get("/api/notes", headers=auth_header)
    assert response.status_code == 200
    data = response.get_json()
    assert data[0]["title"] == "My Note"

def test_update_note(client, auth_header):
    client.post("/api/notes", json={
        "title": "Old Title",
        "content": "Old content"
    }, headers=auth_header)

    note_id = str(Note.objects.first().id)

    response = client.put(f"/api/notes/{note_id}", json={
        "title": "New Title",
        "content": "Updated content"
    }, headers=auth_header)

    assert response.status_code == 200
    assert Note.objects.get(id=note_id).title == "New Title"

def test_delete_note(client, auth_header):
    client.post("/api/notes", json={
        "title": "To Delete",
        "content": "To be deleted"
    }, headers=auth_header)

    note_id = str(Note.objects.first().id)
    response = client.delete(f"/api/notes/{note_id}", headers=auth_header)
    assert response.status_code == 200
    assert Note.objects(id=note_id).first() is None

def test_search_note(client, auth_header):
    client.post("/api/notes", json={
        "title": "Searchable Note",
        "content": "Important content"
    }, headers=auth_header)

    response = client.get("/api/notes/Search", headers=auth_header)
    assert response.status_code == 200
    data = response.get_json()
    assert any("Searchable Note" in note["title"] for note in data)
