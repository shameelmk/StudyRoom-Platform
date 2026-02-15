# Study Room Platform

Backend for a Combined Study Platform where students can create profiles, join study rooms, and share materials.

## Features
-   **User Management**: Registration, Login (JWT), Profile management.
-   **Study Rooms**: Create, search, join, and leave study rooms.
-   **Material Sharing**: Upload (PDF) and view study materials within rooms.
-   **Material Reporting**: Report materials.

## Tech Stack
-   **Language**: Python 3.10+
-   **Framework**: FastAPI
-   **Database**: PostgreSQL
-   **ORM**: SQLAlchemy 2.0
-   **Validation**: Pydantic v2
-   **Migrations**: Alembic
-   **Containerization**: Docker & Docker Compose

## Local Setup Guide

### Prerequisites
-   Docker & Docker Compose
-   Python 3.10+ (if running locally without Docker)
-   [uv](https://github.com/astral-sh/uv) (Recommended) or pip

### 1. Environment Setup
Copy the example environment file:
```bash
cp .env.example .env
```
Update `.env` with your desired credentials if needed (defaults work for local docker).

### 2. Start Database
Run PostgreSQL using Docker Compose:
```bash
docker-compose up -d db
```

### 3. Install Dependencies
Using `uv`:
```bash
uv sync
source .venv/bin/activate
```
Or using `pip` and `venv`:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt # Note: project uses pyproject.toml, so: pip install .
```

### 4. Run Migrations
Apply database schema changes:
```bash
alembic upgrade head
```

### 5. Run the Application
Start the development server:
```bash
fastapi dev app/main.py
```
Or using uvicorn directly:
```bash
uvicorn app.main:app --reload
```

### 6. Access API Documentation
Open your browser to:
-   **Swagger UI**: [http://localhost:8000/api/v1/docs](http://localhost:8000/api/v1/docs)