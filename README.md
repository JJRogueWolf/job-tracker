
# Job Tracker

A full-stack web application built to organise job applications, track recruitment progress, and manage applications from a single dashboard.

Built using Python, FastAPI, PostgreSQL, and vanilla JavaScript. The application is containerised with Docker and deployed on Railway.

## Live Demo

**Application:** https://job-tracker-production-349d8a99.up.railway.app/

**API Documentation:** https://job-tracker-production-349d8a99.up.railway.app/docs

**GitHub:** https://github.com/JJRogueWolf/job-tracker

> Note: This is a public demonstration application with shared data. Authentication has not been implemented. Please use fictional application details.

## Features

- Add new job applications with company, position, status, and application date
- Edit and delete existing applications
- Track applications through Applied, Interview, Offer, and Rejected statuses
- Search applications by company or position
- Filter applications by status
- View application statistics on the dashboard
- Automatically sort applications by application date
- Store application data in PostgreSQL
- Validate API requests using Pydantic
- Manage database schema changes with Alembic
- Automatically update record timestamps
- Access interactive REST API documentation

## Tech Stack

| Category | Technology |
|----------|------------|
| Frontend | HTML5, CSS3, JavaScript |
| Backend | Python 3.11, FastAPI |
| Validation | Pydantic |
| ORM | SQLAlchemy |
| Database | PostgreSQL |
| Database Driver | psycopg |
| Migrations | Alembic |
| Testing | pytest, FastAPI TestClient |
| Containerisation | Docker |
| Hosting | Railway |
| Version Control | Git, GitHub |

## Architecture

The application follows a client-server architecture:

1. The frontend sends HTTP requests to the FastAPI backend.
2. FastAPI validates incoming data using Pydantic.
3. SQLAlchemy handles database operations.
4. PostgreSQL stores application records.
5. FastAPI returns JSON responses.
6. JavaScript updates the dashboard with the latest data.

The frontend and backend are served from the same application, so a separate frontend hosting service is not required.

## Getting Started

### Prerequisites

Make sure you have installed:

- Python 3.11 or later
- PostgreSQL
- Git

### 1. Clone the repository

```bash
git clone https://github.com/JJRogueWolf/job-tracker.git
cd job-tracker/backend
```

### 2. Create a virtual environment

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure PostgreSQL

Create a local PostgreSQL database named `job_tracker`.

Set the `DATABASE_URL` environment variable.

On macOS or Linux:

```bash
export DATABASE_URL="postgresql+psycopg://localhost/job_tracker"
```

On Windows PowerShell:

```powershell
$env:DATABASE_URL="postgresql+psycopg://localhost/job_tracker"
```

These examples assume your local PostgreSQL setup allows a connection without an explicit username or password. If your installation requires credentials, use:

```text
postgresql+psycopg://USERNAME:PASSWORD@localhost:5432/job_tracker
```

Do not commit database credentials to GitHub.

### 5. Apply database migrations

```bash
python -m alembic upgrade head
```

This creates the required database schema and applies subsequent changes.

### 6. Start the application

```bash
python -m uvicorn main:app --reload
```

Open the application in your browser:

http://127.0.0.1:8000

Interactive API documentation:

http://127.0.0.1:8000/docs

## REST API

The backend exposes the following endpoints:

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/jobs` | Retrieve all applications |
| GET | `/jobs/{id}` | Retrieve an application by ID |
| POST | `/jobs` | Create a new application |
| PATCH | `/jobs/{id}` | Update an existing application |
| DELETE | `/jobs/{id}` | Delete an application |

### Example: Create an application

Request:

```http
POST /jobs
Content-Type: application/json
```

```json
{
  "company": "Example Company",
  "position": "Software Engineer",
  "status": "Applied",
  "appliedDate": "2026-11-17"
}
```

### Application statuses

The API accepts four statuses:

- `Applied`
- `Interview`
- `Offer`
- `Rejected`

Invalid status values and blank required fields are rejected by the backend.

## Database

Application records are stored in PostgreSQL.

The database model includes:

| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Unique application identifier |
| company | String | Company name |
| position | String | Job title |
| status | String | Current application status |
| appliedDate | Date | Date of application |
| createdAt | DateTime | Record creation timestamp |
| updatedAt | DateTime | Last update timestamp |

SQLAlchemy manages database operations, while Alembic manages schema migrations.

## Testing

The backend includes automated API tests using pytest and FastAPI TestClient.

The tests cover application endpoints, request validation, and database operations.

Create a separate PostgreSQL database named `job_tracker_test` for testing.

From the `backend` directory, run:

```bash
python -m pytest -v
```

The project currently includes eight passing API tests.

## Docker and Railway Deployment

The application is deployed to Railway using a Dockerfile.

The deployment uses:

- A Python 3.11 Docker image
- Dependencies installed from `backend/requirements.txt`
- Railway PostgreSQL for persistent storage
- A `DATABASE_URL` environment variable referencing the PostgreSQL service
- Alembic migrations executed before the application starts
- Uvicorn serving FastAPI and the frontend

The container starts using the following process:

```bash
python -m alembic upgrade head
python -m uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
```

Railway provides the public HTTPS domain and runtime port.

## Future Improvements

- User authentication and individual accounts
- Private application records for each user
- Pagination for large application lists
- Additional automated frontend tests
- Improved accessibility
- Deployment health checks and monitoring

## Author

**Jobin Joseph**

GitHub: https://github.com/JJRogueWolf

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.