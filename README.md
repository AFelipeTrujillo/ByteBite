# ByteBite
**A Personal Recipe Manager and Smart Shopping List Generator.**

ByteBite is built using **Clean Architecture** principles to ensure the core business logic remains independent of external frameworks, databases, or UI details.

## Architecture Overview
The project is divided into four main layers:

* **Domain**: Pure Python entities, Value Objects, and Repository Interfaces. No dependencies on external libraries.
* **Application**: Use Cases (Interactors) and DTOs (Data Transfer Objects). This layer coordinates the flow of data.
* **Infrastructure**: Framework-specific implementations (FastAPI, MongoDB, JWT, Pydantic Schemas).
* **Delivery**: HTTP Controllers and API definitions.



## Tech Stack
- **Language**: Python 3.12+
- **Framework**: FastAPI
- **Database**: MongoDB (via Motor for async support)
- **Security**: JWT (PyJWT) and Bcrypt (Passlib)
- **Testing**: Pytest & Pytest-Mock

## Getting Started

### Prerequisites
- Python 3.12 installed
- MongoDB instance running (locally or via Docker)

### Installation
1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd ByteBite
   ```
2. Install dependencies:
    ```bash
   pip install .
   ```

### Database Seeding
To initialize the system with default ingredients and an admin user:

```bash
python -m src.Infrastructure.Persistence.Scripts.seed_ingredients
python -m src.Infrastructure.Persistence.Scripts.create_admin_user
```

### Running the API
```bash
uvicorn main:app --reload
```

### Testing
```bash
pytest
```

### Security Policy
All endpoints (except login) are protected. To access them:
1. Authenticate via `POST /api/v1/auth/login`.
2. Use the returned `access_token` as a Bearer token in the `Authorization` header. 