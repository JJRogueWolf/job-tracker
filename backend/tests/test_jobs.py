
import pytest
from uuid import uuid4

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from database import Base, get_db
from main import app
import models

TEST_DATABASE_URL = "postgresql+psycopg:///job_tracker_test"

test_engine = create_engine(
    TEST_DATABASE_URL,
    poolclass=NullPool
)

TestSessionLocal = sessionmaker(bind=test_engine)


@pytest.fixture
def client():
    # Create tables in the separate test database
    Base.metadata.create_all(bind=test_engine)

    def override_get_db():
        with TestSessionLocal() as db:
            yield db

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()
        Base.metadata.drop_all(bind=test_engine)


def sample_job():
    return {
        "company": "Google",
        "position": "Software Engineer",
        "status": "Applied",
        "appliedDate": "2026-11-17"
    }


def test_create_job(client):
    response = client.post("/jobs", json=sample_job())

    assert response.status_code == 201
    assert response.json()["company"] == "Google"
    assert "id" in response.json()


def test_get_jobs(client):
    client.post("/jobs", json=sample_job())

    response = client.get("/jobs")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_update_job(client):
    created = client.post("/jobs", json=sample_job())
    job_id = created.json()["id"]

    response = client.patch(
        f"/jobs/{job_id}",
        json={"status": "Interview"}
    )

    assert response.status_code == 200
    assert response.json()["status"] == "Interview"


def test_delete_job(client):
    created = client.post("/jobs", json=sample_job())
    job_id = created.json()["id"]

    response = client.delete(f"/jobs/{job_id}")

    assert response.status_code == 204
    assert client.get(f"/jobs/{job_id}").status_code == 404


def test_invalid_status(client):
    job = sample_job()
    job["status"] = "Banana"

    response = client.post("/jobs", json=job)

    assert response.status_code == 422


def test_blank_company(client):
    job = sample_job()
    job["company"] = "   "

    response = client.post("/jobs", json=job)

    assert response.status_code == 422


def test_null_patch(client):
    created = client.post("/jobs", json=sample_job())
    job_id = created.json()["id"]

    response = client.patch(
        f"/jobs/{job_id}",
        json={"company": None}
    )

    assert response.status_code == 422


def test_missing_job(client):
    response = client.get(f"/jobs/{uuid4()}")

    assert response.status_code == 404
