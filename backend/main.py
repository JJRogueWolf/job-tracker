import os
from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel, Field
from datetime import date
from uuid import UUID, uuid4

from typing import Annotated
from typing import Literal
from pydantic import field_validator

from pathlib import Path
from fastapi.staticfiles import StaticFiles

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from pydantic import ConfigDict

from fastapi.middleware.cors import CORSMiddleware

from database import get_db
from models import JobDB

app = FastAPI()

allowed_origins = os.environ.get(
    "FRONTEND_ORIGINS",
    "http://127.0.0.1:5500,http://localhost:5500"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["Content-Type"]
)

DbSession = Annotated[Session, Depends(get_db)]

JobStatus = Literal[
    "Applied",
    "Interview",
    "Offer",
    "Rejected"
]

class JobCreate(BaseModel):
    company: str = Field(min_length=1, max_length=200)
    position: str = Field(min_length=1, max_length=200)
    status: JobStatus = "Applied"
    appliedDate: date

    @field_validator("company", "position")
    @classmethod
    def validate_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("This field cannot be empty")
        return value


class JobUpdate(BaseModel):
    company: str | None = Field(default=None, min_length=1, max_length=200)
    position: str | None = Field(default=None, min_length=1, max_length=200)
    status: JobStatus | None = None
    appliedDate: date | None = None

    @field_validator("company", "position", "status", "appliedDate")
    @classmethod
    def reject_null(cls, value):
        if value is None:
            raise ValueError("This field cannot be null")
        return value

    @field_validator("company", "position")
    @classmethod
    def validate_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("This field cannot be empty")
        return value

class Job(JobCreate):
    id: UUID
    model_config = ConfigDict(from_attributes=True)


# @app.get("/")
# def home():
#     return {"message": "Job Tracker API is running"}

@app.get("/jobs", response_model=list[Job])
def get_jobs(db: DbSession):
    statement = select(JobDB).order_by(
        JobDB.appliedDate.desc(),
        JobDB.createdAt.desc(),
        JobDB.id.desc()
    )

    return db.scalars(statement).all()


@app.post("/jobs", response_model=Job, status_code=201)
def create_job(job: JobCreate, db: DbSession):
    new_job = JobDB(**job.model_dump())

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return new_job

@app.get("/jobs/{job_id}", response_model=Job)
def get_job(job_id: UUID, db: DbSession):
    job = db.get(JobDB, job_id)

    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    return job



@app.patch("/jobs/{job_id}", response_model=Job)
def update_job(job_id: UUID, updates: JobUpdate, db: DbSession):
    job = db.get(JobDB, job_id)

    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    update_data = updates.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(job, field, value)

    db.commit()
    db.refresh(job)

    return job


@app.delete("/jobs/{job_id}", status_code=204)
def delete_job(job_id: UUID, db: DbSession):
    job = db.get(JobDB, job_id)

    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    db.delete(job)
    db.commit()

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"

app.mount(
    "/",
    StaticFiles(directory=FRONTEND_DIR, html=True),
    name="frontend"
)