from pydantic import BaseModel, Field, ConfigDict

class BookBase(BaseModel):
    title: str = Field(..., json_schema_extra={"example": "The Great Gatsby"})
    author: str = Field(..., json_schema_extra={"example": "F. Scott Fitzgerald"})
    publication_year: int = Field(..., json_schema_extra={"example": 1925})

    model_config = ConfigDict(from_attributes=True)

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int

class ReviewBase(BaseModel):
    reviewer_name: str = Field(..., json_schema_extra={"example": "John Doe"})
    comment: str = Field(..., json_schema_extra={"example": "A masterpiece of American literature"})
    rating: int = Field(..., json_schema_extra={"example": 5}, ge=1, le=5)

    model_config = ConfigDict(from_attributes=True)

class ReviewCreate(ReviewBase):
    pass

class Review(ReviewBase):
    id: int
    book_id: int