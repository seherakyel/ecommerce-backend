# ShopNova — E-Commerce Backend

A full-stack e-commerce application built with **FastAPI**, **PostgreSQL**, and **React**. This repository contains the backend API, which powers product browsing, a hierarchical category system, authentication, cart, orders, favorites, and address management.

**Live Demo:** [ecommerce-frontend-rho-one.vercel.app](https://ecommerce-frontend-rho-one.vercel.app)
**API Base URL:** [ecommerce-backend-tjxj.onrender.com](https://ecommerce-backend-tjxj.onrender.com)

---

## Features

- **JWT Authentication** — Register, login, and protected endpoints. Passwords are hashed with bcrypt; access is controlled via token verification.
- **Hierarchical Categories** — A three-level category tree built with a self-referencing model.
- **Product Search & Filtering** — Search products by name and filter by category via query parameters.
- **Shopping Cart** — Add, update quantity, and remove items, tied to the authenticated user.
- **Orders** — Place orders from the cart with a selected delivery address, and view order history.
- **Favorites** — Add and remove favorite products.
- **Address Management** — Full CRUD for user delivery addresses.
- **Automated Tests** — Unit and integration tests written with pytest.
- **Dockerized** — Runs with a single command using Docker Compose (backend + PostgreSQL).

---

## Tech Stack

| Layer            | Technology                               |
| ---------------- | ---------------------------------------- |
| Backend          | FastAPI (Python)                         |
| Database         | PostgreSQL                               |
| ORM              | SQLAlchemy                               |
| Auth             | JWT (python-jose), bcrypt                |
| Validation       | Pydantic                                 |
| Testing          | pytest, FastAPI TestClient               |
| Containerization | Docker, Docker Compose                   |
| Deployment       | Render (backend + DB), Vercel (frontend) |

---

## Architecture

```
┌─────────────┐        HTTPS        ┌──────────────┐        ┌──────────────┐
│   React     │  ───────────────>   │   FastAPI    │  ───>  │  PostgreSQL  │
│  (Vercel)   │   REST API calls    │   (Render)   │        │   (Render)   │
└─────────────┘                     └──────────────┘        └──────────────┘
     Frontend                          Backend API              Database

- The frontend calls the backend over REST, sending a JWT in the Authorization header for protected routes.
- The backend validates the token, applies business logic, and reads/writes to PostgreSQL via SQLAlchemy.
```

---

## Getting Started

### Option 1 — Run with Docker (recommended)

The easiest way to run the backend and database together:

```bash
docker-compose up --build
```

This starts the FastAPI backend and a PostgreSQL instance, wired together automatically. The API will be available at `http://localhost:8000`.

### Option 2 — Run locally

**Requirements:** Python 3.12+, PostgreSQL

```bash
# Clone the repository
git clone https://github.com/seherakyel/ecommerce-backend.git
cd ecommerce-backend/backend

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables (see below), then run:
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`, and interactive API docs at `http://localhost:8000/docs`.

### Environment Variables

| Variable       | Description                       | Example                                      |
| -------------- | --------------------------------- | -------------------------------------------- |
| `DATABASE_URL` | PostgreSQL connection string      | `postgresql://user:pass@localhost/ecommerce` |
| `SECRET_KEY`   | Secret key for signing JWT tokens | `your-secret-key`                            |
| `FRONTEND_URL` | Allowed frontend origin (CORS)    | `https://your-frontend.vercel.app`           |

---

## Running Tests

```bash
python3 -m pytest -v
```

Tests use an in-memory SQLite database, so they never touch your development or production data. The suite includes:

- **Unit tests** — registration, login, and rejection of invalid credentials.
- **Integration tests** — the full register → login → authenticated access flow, and rejection of unauthorized requests.

---

## API Overview

Interactive documentation is available at `/docs` when the server is running.

| Method | Endpoint           | Description                     | Auth |
| ------ | ------------------ | ------------------------------- | ---- |
| POST   | `/auth/register`   | Register a new user             | No   |
| POST   | `/auth/login`      | Log in and receive a JWT        | No   |
| GET    | `/auth/me`         | Get current user profile        | Yes  |
| PATCH  | `/auth/me`         | Update current user profile     | Yes  |
| GET    | `/products/`       | List products (search & filter) | No   |
| GET    | `/products/{id}`   | Product detail                  | No   |
| GET    | `/categories/`     | List categories (by parent)     | No   |
| POST   | `/cart/items`      | Add item to cart                | Yes  |
| GET    | `/cart/`           | View cart                       | Yes  |
| PATCH  | `/cart/items/{id}` | Update item quantity            | Yes  |
| DELETE | `/cart/items/{id}` | Remove item from cart           | Yes  |
| POST   | `/orders/`         | Place an order                  | Yes  |
| GET    | `/orders/`         | Order history                   | Yes  |
| POST   | `/favorites/`      | Add a favorite                  | Yes  |
| GET    | `/favorites/`      | List favorites                  | Yes  |
| DELETE | `/favorites/{id}`  | Remove a favorite               | Yes  |
| GET    | `/addresses/`      | List addresses                  | Yes  |
| POST   | `/addresses/`      | Add an address                  | Yes  |
| PATCH  | `/addresses/{id}`  | Update an address               | Yes  |
| DELETE | `/addresses/{id}`  | Delete an address               | Yes  |

---

## Project Structure

```
backend/
├── main.py            # App entry point, CORS, router registration
├── database.py        # Database connection and session
├── models.py          # SQLAlchemy models
├── schemas.py         # Pydantic schemas
├── crud.py            # Database operations
├── auth.py            # Password hashing and JWT logic
├── dependencies.py    # Auth dependency (get_current_user)
├── routers/           # API route modules
├── conftest.py        # Test setup (fixtures, test DB)
├── test_*.py          # Unit and integration tests
├── Dockerfile         # Backend container definition
└── docker-compose.yml # Backend + PostgreSQL orchestration
```

---

