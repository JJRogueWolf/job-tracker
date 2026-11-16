from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel, Field
from datetime import date
from uuid import UUID, uuid4

app = FastAPI()

jobs = []


class JobCreate(BaseModel):
    company: str = Field(min_length=1)
    position: str = Field(min_length=1)
    status: str = "Applied"
    appliedDate: date


class Job(JobCreate):
    id: UUID

class JobUpdate(BaseModel):
    company: str | None = Field(default=None, min_length=1)
    position: str | None = Field(default=None, min_length=1)
    status: str | None = None
    appliedDate: date | None = None


@app.get("/")
def home():
    return {"message": "Job Tracker API is running"}

@app.get("/jobs", response_model = list[Job])
def get_jobs():
    return jobs


@app.post("/jobs", response_model=Job, status_code=status.HTTP_201_CREATED)
def create_job(job: JobCreate):
    new_job = Job(
        id=uuid4(),
        **job.model_dump()
    )

    jobs.append(new_job)

    return new_job

@app.get("/jobs/{job_id}", response_model=Job)
def get_job(job_id: UUID):
    for job in jobs:
        if job.id == job_id:
            return job

    raise HTTPException(
        status_code=404,
        detail="Job not found"
    )


@app.patch("/jobs/{job_id}", response_model=Job)
def update_job(job_id: UUID, updates: JobUpdate):
    for index, job in enumerate(jobs):
        if job.id == job_id:
            update_data = updates.model_dump(exclude_unset=True)

            updated_job = job.model_copy(update=update_data)

            jobs[index] = updated_job

            return updated_job

    raise HTTPException(
        status_code=404,
        detail="Job not found"
    )

@app.delete("/jobs/{job_id}", status_code=204)
def delete_job(job_id: UUID):
    for index, job in enumerate(jobs):
        if job.id == job_id:
            jobs.pop(index)
            return

    raise HTTPException(
        status_code=404,
        detail="Job not found"
    )

