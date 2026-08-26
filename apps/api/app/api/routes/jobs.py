from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..core.security import get_current_user
from ..db import get_db
from ..models import Job, User
from ..schemas import JobCreate

router = APIRouter()

@router.post("")
def create_job(payload: JobCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if user.role != "admin":
        raise HTTPException(403, "Admin access required")
    job = Job(**payload.model_dump())
    db.add(job); db.commit(); db.refresh(job)
    return {"id": str(job.id), **payload.model_dump()}

@router.get("")
def list_jobs(q: str | None = None, db: Session = Depends(get_db)):
    stmt = select(Job).order_by(Job.created_at.desc()).limit(100)
    jobs = list(db.scalars(stmt))
    if q:
        ql = q.lower()
        jobs = [j for j in jobs if ql in j.title.lower() or ql in j.company.lower() or ql in j.description.lower()]
    return [{"id": str(j.id), "title": j.title, "company": j.company, "description": j.description, "location": j.location, "url": j.url, "required_skills": j.required_skills} for j in jobs]

@router.get("/{job_id}")
def get_job(job_id: str, db: Session = Depends(get_db)):
    job = db.get(Job, job_id)
    if not job: raise HTTPException(404, "Job not found")
    return {"id": str(job.id), "title": job.title, "company": job.company, "description": job.description, "location": job.location, "url": job.url, "required_skills": job.required_skills}
