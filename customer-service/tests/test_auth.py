# tests/test_auth.py
import pytest
from app import create_app, db
from app.models import User

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "JWT_SECRET_KEY": "test-secret",
    })
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_user_registration(client, app):
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass"
    }
    response = client.post("/api/auth/register", json=data)
    assert response.status_code == 201
    assert response.json["message"] == "User created successfully"

    # Try registering with the same username
    response_dup = client.post("/api/auth/register", json=data)
    assert response_dup.status_code == 400
    assert "Username already exists" in response_dup.json["message"] or "Email already exists" in response_dup.json["message"]

    # Check user in database
    with app.app_context():
        user = User.query.filter_by(username="testuser").first()
        assert user is not None
        assert user.email == "test@example.com"
        assert user.check_password("testpass")

def test_user_registration_missing_fields(client):
    # Missing username
    data = {"email": "a@b.com", "password": "123"}
    resp = client.post("/api/auth/register", json=data)
    assert resp.status_code == 400

    # Missing email
    data = {"username": "abc", "password": "123"}
    resp = client.post("/api/auth/register", json=data)
    assert resp.status_code == 400

    # Missing password
    data = {"username": "abc", "email": "a@b.com"}
    resp = client.post("/api/auth/register", json=data)
    assert resp.status_code == 400

def test_user_login_success(client, app):
    # Register user first
    data = {
        "username": "loginuser",
        "email": "login@example.com",
        "password": "loginpass"
    }
    client.post("/api/auth/register", json=data)
    # Attempt login
    login_data = {
        "username": "loginuser",
        "password": "loginpass"
    }
    resp = client.post("/api/auth/login", json=login_data)
    assert resp.status_code == 200
    assert "access_token" in resp.json

def test_user_login_invalid_credentials(client, app):
    # Register user
    data = {
        "username": "baduser",
        "email": "bad@example.com",
        "password": "badpass"
    }
    client.post("/api/auth/register", json=data)
    # Wrong password
    resp = client.post("/api/auth/login", json={"username": "baduser", "password": "wrongpass"})
    assert resp.status_code == 401
    assert "Invalid credentials" in resp.json["message"]

def test_user_profile_access(client, app):
    # Register user
    data = {
        "username": "profileuser",
        "email": "profile@example.com",
        "password": "profilepass"
    }
    client.post("/api/auth/register", json=data)

    # Login to get JWT token
    login_resp = client.post(
        "/api/auth/login",
        json={"username": "profileuser", "password": "profilepass"}
    )
    print("Login response JSON:", login_resp.get_json())
    token = login_resp.get_json()["access_token"]
    print("Access token:", token)

    # Access profile with valid token
    resp = client.get(
        "/api/auth/profile",
        headers={"Authorization": f"Bearer {token}"}
    )
    print("Profile response status:", resp.status_code)
    print("Profile response JSON:", resp.get_json())

    assert resp.status_code == 200
    assert resp.get_json()["username"] == "profileuser"
    assert resp.get_json()["email"] == "profile@example.com"