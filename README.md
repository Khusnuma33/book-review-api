# Project API

##  Setup

### Prerequisites
- Python 3.9+
- PostgreSQL 13+
- pip 21+

### Installation
```bash
# Clone repository
git clone https://github.com/Khusnuma33/book-review-api
cd book-review-api

# Create virtual environment (Linux/macOS)
python3 -m venv venv
source venv/bin/activate

# Create virtual environment (Windows)
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt



#Run migrations
alembic upgrade head

#Running the Service
uvicorn app.main:app --reload

#Running Tests
pytest test_api.py -v
