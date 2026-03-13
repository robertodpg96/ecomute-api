# EcoMute API

A production-style electric bike rental REST API built incrementally across 5 labs as part of the **Advanced Programming with Python** course at IE University (MCSBT, FEB-2026).

Each lab introduces a new layer of the stack — from data validation to persistence, security, and automated testing.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Lab Progression](#lab-progression)
- [Setup & Installation](#setup--installation)
- [Running the API](#running-the-api)
- [API Endpoints](#api-endpoints)
- [Authentication Flow](#authentication-flow)
- [Running Tests](#running-tests)
- [Business Rules](#business-rules)

---

## Project Overview

EcoMute is an e-bike sharing platform API. Users can register, log in, and rent available bikes. Admins can manage stations and view system stats. The system enforces real-world constraints such as minimum battery levels for rentals and role-based access control.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| Database | SQLite (via SQLAlchemy 2.0 async + aiosqlite) |
| Data Validation | Pydantic v2 |
| Authentication | JWT (python-jose) + OAuth2 Bearer |
| Password Hashing | passlib + bcrypt |
| Testing | pytest + pytest-asyncio + httpx |
| Server | Uvicorn |

---

## Project Structure

```
lab7/
├── src/
│   ├── dependencies.py               # get_current_user dependency
│   └── app/
│       ├── main.py                   # FastAPI app + lifespan startup
│       ├── data/
│       │   ├── database.py           # Async engine, session, get_db
│       │   ├── models/
│       │   │   └── models.py         # SQLAlchemy ORM: User, Bike, Rental
│       │   └── data_sources/
│       │       ├── bikes_data_source.py
│       │       └── users_data_source.py
│       ├── models/                   # Pydantic schemas (public API interface)
│       │   ├── bikes.py              # BikeCreate, BikeResponse
│       │   ├── rentals.py            # RentalProcessing, RentalResponse, RentalOutcome
│       │   └── user.py               # UserCreate, UserSignUp, UserResponse
│       ├── routers/
│       │   ├── auth.py               # POST /token (OAuth2 login)
│       │   ├── bike.py               # CRUD /bikes
│       │   ├── rentals.py            # POST /rentals (authenticated)
│       │   ├── user.py               # CRUD /users
│       │   ├── admin.py              # GET /admin/stats (admin only)
│       │   └── stations.py           # POST /stations (admin only)
│       ├── security/
│       │   └── security.py           # Password hashing + JWT creation
│       └── services/
│           └── pricing.py            # PricingService (calculate_cost)
├── test/
│   └── app/
│       ├── conftest.py               # Fixtures: in-memory DB, async_client
│       └── services/
│           ├── test_api.py           # Integration tests (bikes endpoints)
│           └── test_logic.py         # Unit tests (PricingService)
├── pytest.ini                        # Pytest config (asyncio_mode = auto)
├── requirements.txt
└── ecomute.db                        # SQLite database (auto-created on startup)
```

---

## Lab Progression

### Lab 3 — Pydantic Power & Data Integrity *(Sessions 5 & 6)*

**Goal:** Stop garbage data from entering the system.

- Introduced Pydantic model **inheritance** (`BikesBase` → `BikeCreate`, `BikeResponse`)
- Added **specialized field types**: `EmailStr` for email validation
- Implemented `@field_validator` on `UserSignUp` to enforce:
  - Password minimum 8 characters
  - Password must be alphanumeric
- Created `RentalOutcome` with a validator rejecting rentals when `battery < 20%`
- Added `RentalProcessing` model used in `POST /rentals`

---

### Lab 4 — Dependency Injection & Architecture *(Sessions 7 & 8)*

**Goal:** Decouple business logic from API logic using FastAPI's `Depends` system.

- Created `BikesDataSource` and `UsersDataSource` classes encapsulating data access
- Introduced provider functions (`get_bike_datasource`, `get_users_datasource`) as DI factories
- Refactored routers to receive data sources via injection instead of hardcoded access
- Created the `PricingService` class (`calculate_cost(minutes)`) to separate pricing logic
- Added the `/admin` router with **router-level dependency scoping** (API key protection on the entire router)

---

### Lab 5 — Persistence with SQLAlchemy & Async IO *(Sessions 9 & 10)*

**Goal:** Replace volatile in-memory mocks with a real persistent database.

- Installed `sqlalchemy` + `aiosqlite` for async SQLite support
- Created `database.py` with:
  - `create_async_engine` pointing at `sqlite+aiosqlite:///./ecomute.db`
  - `async_sessionmaker` for session management
  - `get_db` async generator dependency
- Defined SQLAlchemy ORM models in `models.py`:
  - `User` (id, username, email, hashed_password, role, is_active)
  - `Bike` (id, model, battery, status)
  - `Rental` (id, user_id FK, bike_id FK, created_at, updated_at) — FK uses `ondelete="SET NULL"` to preserve rental history when a user or bike is deleted
- Used a **lifespan context manager** in `main.py` to auto-create tables on startup and dispose the engine on shutdown
- Refactored all routers to use `AsyncSession` + `await db.execute(...)`

---

### Lab 6 — Ironclad Security: Auth & JWT *(Sessions 11 & 12)*

**Goal:** Transition from an open system to a secure, token-based system.

- Added `hashed_password` and `role` columns to the `User` ORM model
- Created `security.py` with:
  - `pwd_context` (bcrypt) for password hashing
  - `verify_password(plain, hashed)` and `get_password_hash(plain)`
  - `create_access_token(data)` — signs a JWT with `HS256` and a 15-minute expiry
- Created `POST /token` endpoint (OAuth2-compatible) that validates credentials and returns a Bearer token
- Created `get_current_user` dependency in `src/dependencies.py`:
  - Reads `Authorization: Bearer <token>` header
  - Decodes and verifies the JWT
  - Fetches the user from the database
- Protected `POST /rentals` and `POST /stations` behind `get_current_user`
- `POST /stations` and `GET /admin/stats` further restrict access to `role == 'admin'`
- `POST /users` uses `UserSignUp` (with password hashing) instead of plain `UserCreate`

---

### Lab 7 — Automated Testing with Pytest *(Sessions 13 & 14)*

**Goal:** Build a safety net. Replace manual Swagger UI testing with automated scripts.

- Configured `pytest.ini` with `asyncio_mode = auto` and `pythonpath = .`
- **Unit tests** (`test/app/services/test_logic.py`):
  - `test_pricing_calculation` — asserts `PricingService(rate=2.0).calculate_cost(10) == 20.0`
  - `test_negative_minutes` — asserts negative input returns `0.0`
- **Test infrastructure** (`test/app/conftest.py`):
  - `test_db_session` fixture — spins up a fresh **in-memory SQLite** database for each test, creates all tables, yields a session, then drops all tables
  - `async_client` fixture — overrides the `get_db` dependency with the test session and provides an `httpx.AsyncClient` pointed at the FastAPI app
- **Integration tests** (`test/app/services/test_api.py`):
  - `test_get_bikes` — inserts a bike via the DB session, asserts `GET /bikes/` returns it
  - `test_read_bike` — inserts a bike, asserts `GET /bikes/{id}` returns correct data
  - `test_no_bike` — asserts `GET /bikes/1` on empty DB returns `404`
  - `test_wrong_bike` — asserts requesting a non-existent ID returns `404`
  - `test_add_bike_ok` — asserts `POST /bikes/` with valid data returns `201`
  - `test_add_bike_wrong_data` — asserts `POST /bikes/` with invalid data returns `422`

---

## Setup & Installation

**Prerequisites:** Python 3.12+

```bash
# 1. Clone / navigate to the project
cd "lab7"

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate       # macOS/Linux
.venv\Scripts\activate          # Windows

# 3. Install dependencies
pip install -r requirements.txt
```

---

## Running the API

```bash
uvicorn src.app.main:app --reload
```

The database file `ecomute.db` is created automatically on first startup.

Interactive docs are available at:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

---

## API Endpoints

### Authentication
| Method | Path | Description | Auth |
|--------|------|-------------|------|
| POST | `/token` | Login — returns JWT Bearer token | None |

### Users
| Method | Path | Description | Auth |
|--------|------|-------------|------|
| GET | `/users/` | List all users | None |
| GET | `/users/{id}` | Get user by ID | None |
| POST | `/users/` | Register a new user (hashes password) | None |
| PUT | `/users/{id}` | Update user | None |
| DELETE | `/users/{id}` | Delete user | None |

### Bikes
| Method | Path | Description | Auth |
|--------|------|-------------|------|
| GET | `/bikes/` | List all bikes (optional `?status=` filter) | None |
| GET | `/bikes/{id}` | Get bike by ID | None |
| POST | `/bikes/` | Create a bike | None |
| PUT | `/bikes/{id}` | Update a bike | None |
| DELETE | `/bikes/{id}` | Delete a bike | None |

### Rentals
| Method | Path | Description | Auth |
|--------|------|-------------|------|
| POST | `/rentals/` | Rent a bike (user taken from token) | Bearer token |

### Admin
| Method | Path | Description | Auth |
|--------|------|-------------|------|
| GET | `/admin/stats` | View admin statistics | Bearer token (admin role) |
| POST | `/stations/` | Create a station | Bearer token (admin role) |

---

## Authentication Flow

```
1. Register:    POST /users/        { username, email, password }
2. Login:       POST /token         form-data: username + password
                ← { access_token, token_type: "bearer" }
3. Use token:   Authorization: Bearer <access_token>
                on any protected endpoint
```

Tokens expire after **15 minutes**. Passwords are never stored in plain text — only bcrypt hashes.

---

## Running Tests

```bash
pytest
```

Tests run against an **in-memory SQLite database** — the production `ecomute.db` is never touched.

```bash
# Verbose output
pytest -v

# Run only unit tests
pytest test/app/services/test_logic.py

# Run only integration tests
pytest test/app/services/test_api.py
```

---

## Business Rules

| Rule | Enforcement |
|------|-------------|
| Bike battery must be ≥ 20% to rent | Validated in `POST /rentals` router |
| Bike must have `status = "available"` to rent | Validated in `POST /rentals` router |
| Password must be ≥ 8 alphanumeric characters | `@field_validator` in `UserSignUp` |
| Email must be a valid address | `EmailStr` type in `UserSignUp` |
| Only `admin` users can create stations | `get_current_user` + role check in `POST /stations` |
| Only `admin` users can view admin stats | `get_current_user` + role check in `GET /admin/stats` |
| Rental history is preserved when a bike/user is deleted | `ondelete="SET NULL"` on FK columns |
| Pricing is calculated as `minutes × base_rate` (min 0) | `PricingService.calculate_cost()` |

---

*Course: Advanced Programming with Python — IE University MCSBT, Term 2 FEB-2026*
*Professor: David Estivariz Pierola*
