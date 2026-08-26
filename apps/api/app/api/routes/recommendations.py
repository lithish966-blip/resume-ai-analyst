from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from ...db import get_db
from ...models import Job, Resume
from ...core.security import current_user

router = APIRouter()

@router.get("/jobs")
def recommended_jobs(limit: int = 10, db: Session = Depends(get_db), user=Depends(current_user)):
    resume = db.scalars(select(Resume).where(Resume.user_id == user.id).order_by(Resume.created_at.desc())).first()
    jobs = db.scalars(select(Job).order_by(Job.created_at.desc()).limit(max(1, min(limit, 50)))).all()
    if not resume:
        return {"items": [{"id": str(j.id), "title": j.title, "company": j.company, "match_score": 0, "reason": "Upload a resume to personalize this recommendation."} for j in jobs]}
    text = resume.raw_text.lower()
    items = []
    for job in jobs:
        skills = [str(x).lower() for x in (job.required_skills or [])]
        score = round(100 * sum(s in text for s in skills) / len(skills), 1) if skills else 50
        items.append({"id": str(job.id), "title": job.title, "company": job.company, "location": job.location, "match_score": score, "reason": "Strong skill overlap" if score >= 70 else "Potential match with skill gaps"})
    return {"items": sorted(items, key=lambda x: x["match_score"], reverse=True)}

@router.get("/skills")
def recommended_skills(db: Session = Depends(get_db), user=Depends(current_user)):
    return {"items": [{"skill": "Docker", "priority": "high"}, {"skill": "AWS", "priority": "high"}, {"skill": "FastAPI", "priority": "medium"}, {"skill": "Redis", "priority": "medium"}]}

@router.get("/careers")
def career_recommendations():
    return {"items": [{"role": "Backend Engineer", "reason": "Strong alignment with Python and API development"}, {"role": "Platform Engineer", "reason": "Add Docker, Kubernetes and cloud skills"}, {"role": "AI Application Engineer", "reason": "Combine Python backend skills with LLM application development"}]}
