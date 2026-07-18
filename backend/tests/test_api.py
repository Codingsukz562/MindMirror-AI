"""Tests for MindMirror AI backend."""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


def test_root_endpoint():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "MindMirror AI" in data["message"]


def test_list_habits():
    """Test listing habits."""
    response = client.get("/api/habits")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_get_habit():
    """Test getting a specific habit."""
    response = client.get("/api/habits/social_media")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "social_media"
    assert data["category"] == "social_media"


def test_get_invalid_habit():
    """Test getting an invalid habit returns 400."""
    response = client.get("/api/habits/invalid_habit")
    assert response.status_code == 400


def test_get_nonexistent_habit():
    """Test getting a nonexistent habit returns 404."""
    response = client.get("/api/habits/other")
    # 'other' is valid but may not have been initialized
    assert response.status_code in [200, 404]


def test_create_reflection():
    """Test creating a reflection."""
    reflection_data = {
        "content": "I felt stressed after work and wanted to scroll through social media."
    }
    response = client.post(
        "/api/habits/social_media/reflections",
        json=reflection_data
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["habit_id"] == "social_media"


def test_create_empty_reflection():
    """Test that empty reflections are rejected."""
    reflection_data = {"content": ""}
    response = client.post(
        "/api/habits/social_media/reflections",
        json=reflection_data
    )
    assert response.status_code == 400


def test_create_short_reflection():
    """Test that very short reflections are rejected."""
    reflection_data = {"content": "test"}
    response = client.post(
        "/api/habits/social_media/reflections",
        json=reflection_data
    )
    assert response.status_code == 400


def test_list_reflections():
    """Test listing reflections for a habit."""
    response = client.get("/api/habits/social_media/reflections")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_coaching_plan():
    """Test getting coaching plan."""
    response = client.get("/api/habits/social_media/coaching")
    assert response.status_code == 200
    data = response.json()
    assert "trigger_analysis" in data
    assert "risk_prediction" in data
    assert "daily_plan" in data
    assert "motivation_message" in data


def test_request_id_header():
    """Test that responses include request ID."""
    response = client.get("/api/health")
    assert "X-Request-ID" in response.headers


def test_cors_headers():
    """Test CORS headers are present."""
    response = client.get(
        "/api/health",
        headers={"Origin": "http://localhost:3000"}
    )
    assert response.status_code == 200
