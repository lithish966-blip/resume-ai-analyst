from pathlib import Path
from uuid import uuid4
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session
from ..core.config import settings
from ..core.security import get_current_user
from ..db import get_db
from ..models import Resume, User
from ..services.parser import clean_text, parse_resume
from ..services.analyzer import analyze_resume
from ...ai.engine import ai_engine

router = APIRouter()
ALLOWED = {"application/pdf": "pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx"}

@router.post("/upload")
async def upload_resume(file: UploadFile = File(...), user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    file_type = ALLOWED.get(file.content_type or "")
    if not file_type:
        raise HTTPException(400, "Only PDF and DOCX resumes are supported")
    data = await file.read()
    if len(data) > settings.max_upload_mb * 1024 * 1024:
        raise HTTPException(413, "Resume file is too large")
    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)
    path = upload_dir / f"{uuid4()}.{file_type}"
    path.write_bytes(data)
    try:
        text = clean_text(parse_resume(str(path), file_type))
        analysis = ai_engine.analyze_resume(text) if ai_engine.client else analyze_resume(text)
    except Exception as exc:
        path.unlink(missing_ok=True)
        raise HTTPException(422, f"Could not parse or analyze resume: {exc}") from exc
    resume = Resume(user_id=user.id, file_name=file.filename or path.name, file_type=file_type, raw_text=text, analysis=analysis)
    db.add(resume)
    db.commit()
    db.refresh(resume)
    path.unlink(missing_ok=True)
    return {"id": str(resume.id), "file_name": resume.file_name, "status": resume.status, "analysis": analysis}

@router.get("")
def list_resumes(user: User = Depends(get_current_user)):
    return [{"id": str(r.id), "file_name": r.file_name, "status": r.status, "analysis": r.analysis} for r in user.resumes]

@router.get("/{resume_id}")
def get_resume(resume_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    resume = db.get(Resume, resume_id)
    if not resume or resume.user_id != user.id:
        raise HTTPException(404, "Resume not found")
    return {"id": str(resume.id), "file_name": resume.file_name, "raw_text": resume.raw_text, "analysis": resume.analysis}

@router.post("/{resume_id}/analyze")
def reanalyze_resume(resume_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    resume = db.get(Resume, resume_id)
    if not resume or resume.user_id != user.id:
        raise HTTPException(404, "Resume not found")
    resume.analysis = ai_engine.analyze_resume(resume.raw_text) if ai_engine.client else analyze_resume(resume.raw_text)
    resume.status = "analyzed"
    db.commit()
    return {"id": str(resume.id), "status": resume.status, "analysis": resume.analysis}
