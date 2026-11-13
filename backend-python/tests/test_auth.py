import pytest
from app.models.user import User

@pytest.mark.asyncio
async def test_register_user(client):
    response = await client.post("/api/auth/register", json={
        "name": "Test User",
        "email": "test@example.com",
        "password": "password123",
        "role": "USER"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    assert data["email"] == "test@example.com"
    assert data["role"] == "USER"
    
    user = await User.find_one(User.email == "test@example.com")
    assert user is not None
    assert user.name == "Test User"


@pytest.mark.asyncio
async def test_duplicate_email(client):
    # First registration
    await client.post("/api/auth/register", json={
        "name": "Test User",
        "email": "test@example.com",
        "password": "password123",
        "role": "USER"
    })
    
    # Second registration
    response = await client.post("/api/auth/register", json={
        "name": "Test User 2",
        "email": "test@example.com",
        "password": "password123",
        "role": "USER"
    })
    
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_login(client):
    # Register
    await client.post("/api/auth/register", json={
        "name": "Test User",
        "email": "login@example.com",
        "password": "password123",
        "role": "USER"
    })
    
    # Login
    response = await client.post("/api/auth/login", json={
        "email": "login@example.com",
        "password": "password123"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    assert data["email"] == "login@example.com"
