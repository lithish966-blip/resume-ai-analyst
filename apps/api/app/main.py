from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.routes import auth, resumes, jobs, matches, skills, recommendations, profile, admin
from .core.config import settings
from .db import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="Resume AI Analyst API", version="1.1.0", description="AI Resume Analyzer, ATS scorer and Job Matcher API", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(resumes.router, prefix="/api/v1/resumes", tags=["resumes"])
app.include_router(jobs.router, prefix="/api/v1/jobs", tags=["jobs"])
app.include_router(matches.router, prefix="/api/v1/matches", tags=["matches"])
app.include_router(skills.router, prefix="/api/v1/skill-gaps", tags=["skill-gaps"])
app.include_router(recommendations.router, prefix="/api/v1/recommendations", tags=["recommendations"])
app.include_router(profile.router, prefix="/api/v1/profile", tags=["profile"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["admin"])

@app.get("/health")
def health():
    return {"status": "ok", "service": "resume-ai-analyst-api", "version": "1.1.0"}
