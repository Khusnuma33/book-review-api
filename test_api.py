from fastapi.testclient import TestClient
from app.main import app
from app.dependencies import cache_service

client = TestClient(app)

def test_create_book():
    """Test book creation endpoint"""
    response = client.post(
        "/api/v1/books/",
        json={"title": "Test Book", "author": "Test Author", "publication_year": 2023}
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Test Book"

def test_get_books():
    """Test getting all books"""
    # First create a book
    client.post(
        "/api/v1/books/",
        json={"title": "Test Book", "author": "Test Author", "publication_year": 2023}
    )
    
    # Then get books
    response = client.get("/api/v1/books/")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_cache_integration():
    """Test cache behavior"""
    cache_service.clear()
    
    # First request (should miss cache)
    response1 = client.get("/api/v1/books/")
    assert response1.status_code == 200
    
    # Second request (should hit cache)
    response2 = client.get("/api/v1/books/")
    assert response2.status_code == 200
    assert response1.json() == response2.json()

# UPDATED TESTS START HERE
def test_create_review():
    # Create a book first
    book_response = client.post(
        "/api/v1/books/",
        json={"title": "Test Book", "author": "Test Author", "publication_year": 2023}
    )
    book_id = book_response.json()["id"]
    
    # Now create review
    response = client.post(
        f"/api/v1/books/{book_id}/reviews",
        json={
            "reviewer_name": "Tester",
            "comment": "Great book!",
            "rating": 5
        }
    )
    assert response.status_code == 201
    assert response.json()["book_id"] == book_id

def test_get_reviews():
    # Create a book first
    book_response = client.post(
        "/api/v1/books/",
        json={"title": "Test Book", "author": "Test Author", "publication_year": 2023}
    )
    book_id = book_response.json()["id"]
    
    # Create a review
    client.post(
        f"/api/v1/books/{book_id}/reviews",
        json={
            "reviewer_name": "Tester",
            "comment": "Great book!",
            "rating": 5
        }
    )
    
    # Get reviews
    response = client.get(f"/api/v1/books/{book_id}/reviews")
    assert response.status_code == 200
    assert len(response.json()) > 0
# UPDATED TESTS END HERE

def test_nonexistent_book_reviews():
    """Test getting reviews for non-existent book"""
    response = client.get("/api/v1/books/999/reviews")
    assert response.status_code == 404
    assert "Book not found" in response.json()["detail"]

def test_create_review_nonexistent_book():
    """Test creating review for non-existent book"""
    response = client.post(
        "/api/v1/books/999/reviews",
        json={
            "reviewer_name": "Tester",
            "comment": "Great book!",
            "rating": 5
        }
    )
    assert response.status_code == 404
    assert "Book not found" in response.json()["detail"]