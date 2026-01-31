"""
Verse API Tests
===============
Tests for verse lookup endpoints.
"""
import pytest


def test_get_verse_by_reference(client):
    """Test verse lookup by reference (e.g., John 3:16)"""
    response = client.get("/api/verses/John%203:16")

    assert response.status_code == 200
    data = response.json()
    assert data["reference"] == "John 3:16"
    assert "greek_text" in data
    assert "english_text" in data


def test_get_verse_invalid_reference(client):
    """Test verse lookup with invalid reference"""
    response = client.get("/api/verses/InvalidBook%201:1")

    assert response.status_code in [400, 404]


def test_get_verse_by_book_code(client):
    """Test verse lookup by book code"""
    # John 3:16 in SBLGNT format
    response = client.get("/api/verses/book/43/3/16")

    assert response.status_code == 200
    data = response.json()
    assert "greek_text" in data


def test_list_books(client):
    """Test listing all NT books"""
    response = client.get("/api/verses/books/list")

    assert response.status_code == 200
    data = response.json()
    assert "books" in data
    assert len(data["books"]) == 27  # NT has 27 books
