from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from ...db import get_db
from ...models import User, Resume, Job
from ...core.security import current_user

router = APIRouter()

def admin_only(user):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user

@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db), user=Depends(current_user)):
    admin_only(user)
    return {"users": db.scalar(select(func.count()).select_from(User)) or 0, "resumes": db.scalar(select(func.count()).select_from(Resume)) or 0, "jobs": db.scalar(select(func.count()).select_from(Job)) or 0, "status": "healthy"}

@router.get("/users")
def users(db: Session = Depends(get_db), user=Depends(current_user)):
    admin_only(user)
    return {"items": [{"id": str(x.id), "email": x.email, "full_name": x.full_name, "role": x.role, "is_active": x.is_active} for x in db.scalars(select(User).order_by(User.created_at.desc())).all()]}

@router.get("/resumes")
def resumes(db: Session = Depends(get_db), user=Depends(current_user)):
    admin_only(user)
    return {"items": [{"id": str(x.id), "user_id": str(x.user_id), "file_name": x.file_name, "status": x.status, "created_at": x.created_at} for x in db.scalars(select(Resume).order_by(Resume.created_at.desc()).limit(100)).all()]}

@router.get("/jobs")
def jobs(db: Session = Depends(get_db), user=Depends(current_user)):
    admin_only(user)
    return {"items": [{"id": str(x.id), "title": x.title, "company": x.company, "location": x.location} for x in db.scalars(select(Job).order_by(Job.created_at.desc()).limit(100)).all()]}

@router.get("/analytics")
def analytics(db: Session = Depends(get_db), user=Depends(current_user)):
    admin_only(user)
    return {"resume_uploads": db.scalar(select(func.count()).select_from(Resume)) or 0, "job_records": db.scalar(select(func.count()).select_from(Job)) or 0, "active_users": db.scalar(select(func.count()).select_from(User).where(User.is_active.is_(True))) or 0}
