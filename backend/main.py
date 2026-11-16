from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel, Field
from datetime import date
from uuid import UUID, uuid4

from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from pydantic import ConfigDict

from database import get_db
from models import JobDB

app = FastAPI()

DbSession = Annotated[Session, Depends(get_db)]

class JobCreate(BaseModel):
    company: str = Field(min_length=1)
    position: str = Field(min_length=1)
    status: str = "Applied"
    appliedDate: date


class Job(JobCreate):
    id: UUID
    model_config = ConfigDict(from_attributes=True)

class JobUpdate(BaseModel):
    company: str | None = Field(default=None, min_length=1)
    position: str | None = Field(default=None, min_length=1)
    status: str | None = None
    appliedDate: date | None = None


@app.get("/")
def home():
    return {"message": "Job Tracker API is running"}

@app.get("/jobs", response_model=list[Job])
def get_jobs(db: DbSession):
    return db.scalars(select(JobDB)).all()


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

