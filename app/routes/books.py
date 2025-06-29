from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import Book, BookCreate, Review, ReviewCreate
from app import crud
from app.dependencies import CacheService, get_cache_service

router = APIRouter(tags=["books"])

@router.post("/books/", response_model=Book, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db, book)

@router.get("/books/", response_model=list[Book])
def read_books(skip: int = 0, limit: int = 100, 
              db: Session = Depends(get_db),
              cache: CacheService = Depends(get_cache_service)):
    cache_key = f"books_{skip}_{limit}"
    
    try:
        cached_books = cache.get(cache_key)
        if cached_books:
            return cached_books
    except Exception as e:
        print(f"Cache error: {str(e)}")

    books = crud.get_books(db, skip, limit)
    
    try:
        cache.set(cache_key, books)
    except Exception:
        pass
        
    return books

@router.get("/books/{book_id}/reviews", response_model=list[Review])
def read_reviews(book_id: int, db: Session = Depends(get_db)):
    # Check if book exists first
    book = crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    reviews = crud.get_reviews(db, book_id)
    return reviews

@router.post("/books/{book_id}/reviews", 
             response_model=Review, 
             status_code=status.HTTP_201_CREATED)
def create_review(book_id: int, review: ReviewCreate, 
                 db: Session = Depends(get_db)):
    # Check if book exists
    book = crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    return crud.create_review(db, review, book_id)