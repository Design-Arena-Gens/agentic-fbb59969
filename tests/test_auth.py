import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.database import Base, engine, get_db
from sqlalchemy.orm import Session

client = TestClient(app)


def test_register_user():
    """Test user registration"""
    response = client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["user"]["email"] == "test@example.com"


def test_register_duplicate_email():
    """Test registration with duplicate email"""
    # First registration
    client.post(
        "/auth/register",
        json={
            "username": "user1",
            "email": "duplicate@example.com",
            "password": "testpass123"
        }
    )

    # Duplicate registration
    response = client.post(
        "/auth/register",
        json={
            "username": "user2",
            "email": "duplicate@example.com",
            "password": "testpass123"
        }
    )
    assert response.status_code == 400


def test_login_user():
    """Test user login"""
    # Register first
    client.post(
        "/auth/register",
        json={
            "username": "logintest",
            "email": "login@example.com",
            "password": "testpass123"
        }
    )

    # Login
    response = client.post(
        "/auth/login",
        json={
            "email": "login@example.com",
            "password": "testpass123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data


def test_login_wrong_password():
    """Test login with wrong password"""
    response = client.post(
        "/auth/login",
        json={
            "email": "login@example.com",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401
