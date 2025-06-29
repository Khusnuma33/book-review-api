import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routes import books
from app.database import engine
from app import models

# Create the lifespan manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables (only for development)
    models.Base.metadata.create_all(bind=engine)
    
    # Print docs URL
    port = os.getenv("PORT", "8000")
    docs_url = f"http://localhost:{port}/docs"
    print("\n" + "="*60)
    print(f"\033[1;92mAPI Documentation: \033[4;97m{docs_url}\033[0m")
    print("\033[93mCtrl+Click the URL above to open Swagger UI\033[0m")
    print("="*60 + "\n")
    yield

# Create a single FastAPI instance with lifespan
app = FastAPI(
    title="Book Review API",
    description="API for managing books and reviews",
    version="0.1.0",
    servers=[{"url": "http://localhost:8000", "description": "Local Server"}],
    lifespan=lifespan
)

# Include your router
app.include_router(books.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Book Review Service"}