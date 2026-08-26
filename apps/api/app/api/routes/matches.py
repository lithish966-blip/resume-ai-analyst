from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..core.security import get_current_user
from ..db import get_db
from ..models import Job, Resume, User
from ..services.analyzer import match_job

router = APIRouter()

@router.get("")
def matches(resume_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    resume = db.get(Resume, resume_id)
    if not resume or resume.user_id != user.id:
        raise HTTPException(404, "Resume not found")
    jobs = list(db.scalars(select(Job).order_by(Job.created_at.desc()).limit(100)))
    results = []
    for job in jobs:
        score = match_job(resume.raw_text, job.required_skills or [], job.description)
        results.append({"job_id": str(job.id), "title": job.title, "company": job.company, **score})
    return sorted(results, key=lambda x: x["overall_score"], reverse=True)[:25]
