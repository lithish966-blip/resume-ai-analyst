# Resume AI Analyst

Production-ready AI Resume Analyzer & Job Matcher.

## Current Status

**Phase 0 — Architecture & Implementation Planning**

The repository has been initialized with the approved architecture and implementation plan. Application code has intentionally **not** been implemented yet.

## Planned Stack

- Frontend: Next.js + TypeScript + Tailwind CSS + shadcn/ui
- Backend: FastAPI + Python
- Database: PostgreSQL + pgvector
- Authentication: JWT + HTTP-only cookies + Argon2id
- Background jobs: Celery + Redis
- Resume parsing: PyMuPDF + python-docx
- AI: Provider-agnostic LLM and embedding services
- Storage: S3-compatible object storage
- Testing: Pytest, Vitest, Playwright
- CI/CD: GitHub Actions
- Deployment: Docker + managed cloud services

## Architecture

```text
Next.js Web App
      |
      v
FastAPI API
  |       |
  v       v
PostgreSQL Redis
+pgvector   |
            v
       Celery Workers
        /    |    \
    Parser  AI  Embeddings
        \    |    /
         S3 / AI Provider
```

## Documentation

- [Architecture & Implementation Plan](docs/architecture/implementation-plan.md)

## Development Principle

The system will use asynchronous processing for expensive resume parsing, AI analysis, embedding generation, and job matching. AI components will be modular and provider-agnostic.

## Repository

GitHub: https://github.com/lithish966-blip/resume-ai-analyst
