from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from auth import get_current_user
from database import get_db
from models.job import Job


router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)


class JobCreate(BaseModel):
    title: str
    company: str | None = None
    description: str


@router.post("/")
def create_job(
    job_data: JobCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    job = Job(
        user_id=current_user["id"],
        title=job_data.title,
        company=job_data.company,
        description=job_data.description
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return {
        "message": "Job created successfully",
        "job": {
            "id": job.id,
            "title": job.title,
            "company": job.company,
            "description": job.description
        }
    }


@router.get("/")
def get_jobs(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    jobs = (
        db.query(Job)
        .filter(Job.user_id == current_user["id"])
        .all()
    )

    return {
        "jobs": [
            {
                "id": job.id,
                "title": job.title,
                "company": job.company,
                "description": job.description
            }
            for job in jobs
        ]
    }


@router.get("/{job_id}")
def get_job(
    job_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    job = (
        db.query(Job)
        .filter(
            Job.id == job_id,
            Job.user_id == current_user["id"]
        )
        .first()
    )

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    return {
        "id": job.id,
        "title": job.title,
        "company": job.company,
        "description": job.description
    }