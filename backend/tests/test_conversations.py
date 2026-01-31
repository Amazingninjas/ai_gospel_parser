"""
Conversation API Tests
======================
Tests for conversation history endpoints.
"""
import pytest


def test_create_conversation(client, auth_headers):
    """Test creating a new conversation"""
    response = client.post(
        "/api/conversations",
        headers=auth_headers,
        json={
            "title": "Test Conversation",
            "messages": [
                {"role": "user", "content": "Hello"}
            ]
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Conversation"
    assert len(data["messages"]) == 1


def test_create_conversation_auto_title(client, auth_headers):
    """Test conversation title auto-generation"""
    response = client.post(
        "/api/conversations",
        headers=auth_headers,
        json={
            "messages": [
                {"role": "user", "content": "What does agape mean in Greek?"}
            ]
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert "agape" in data["title"].lower()


def test_list_conversations(client, auth_headers):
    """Test listing user's conversations"""
    # Create a conversation first
    client.post(
        "/api/conversations",
        headers=auth_headers,
        json={"title": "Test"}
    )

    response = client.get("/api/conversations", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_conversation_by_id(client, auth_headers):
    """Test getting specific conversation"""
    # Create conversation
    create_response = client.post(
        "/api/conversations",
        headers=auth_headers,
        json={"title": "Test"}
    )
    conv_id = create_response.json()["id"]

    # Get conversation
    response = client.get(f"/api/conversations/{conv_id}", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == conv_id


def test_update_conversation(client, auth_headers):
    """Test updating conversation"""
    # Create conversation
    create_response = client.post(
        "/api/conversations",
        headers=auth_headers,
        json={"title": "Original Title"}
    )
    conv_id = create_response.json()["id"]

    # Update conversation
    response = client.put(
        f"/api/conversations/{conv_id}",
        headers=auth_headers,
        json={"title": "Updated Title"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"


def test_append_message(client, auth_headers):
    """Test appending message to conversation"""
    # Create conversation
    create_response = client.post(
        "/api/conversations",
        headers=auth_headers,
        json={"title": "Test"}
    )
    conv_id = create_response.json()["id"]

    # Append message
    response = client.post(
        f"/api/conversations/{conv_id}/messages",
        headers=auth_headers,
        params={
            "role": "user",
            "content": "New message"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data["messages"]) == 1


def test_delete_conversation(client, auth_headers):
    """Test deleting conversation"""
    # Create conversation
    create_response = client.post(
        "/api/conversations",
        headers=auth_headers,
        json={"title": "To Delete"}
    )
    conv_id = create_response.json()["id"]

    # Delete conversation
    response = client.delete(f"/api/conversations/{conv_id}", headers=auth_headers)

    assert response.status_code == 204

    # Verify deletion
    get_response = client.get(f"/api/conversations/{conv_id}", headers=auth_headers)
    assert get_response.status_code == 404


def test_conversation_requires_auth(client):
    """Test conversation endpoints require authentication"""
    response = client.get("/api/conversations")
    assert response.status_code == 401
