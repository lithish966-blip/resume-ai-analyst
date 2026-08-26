from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from ...db import get_db
from ...models import Resume, Job
from ...core.security import current_user

router = APIRouter()

@router.get("")
def skill_gaps(resume_id: str | None = None, job_id: str | None = None, db: Session = Depends(get_db), user=Depends(current_user)):
    resume = db.scalar(select(Resume).where(Resume.id == resume_id, Resume.user_id == user.id)) if resume_id else db.scalars(select(Resume).where(Resume.user_id == user.id).order_by(Resume.created_at.desc())).first()
    if not resume:
        return {"items": [], "message": "Upload a resume to calculate skill gaps."}
    job = db.get(Job, job_id) if job_id else None
    required = [str(x).strip().lower() for x in (job.required_skills if job else [])]
    text = resume.raw_text.lower()
    missing = [skill for skill in required if skill and skill not in text]
    return {"resume_id": str(resume.id), "job_id": str(job.id) if job else None, "gaps": [{"skill": x, "priority": "high" if i < 2 else "medium", "recommendation": f"Build a practical project demonstrating {x}."} for i, x in enumerate(dict.fromkeys(missing))]}
