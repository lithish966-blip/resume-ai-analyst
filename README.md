# Resume AI Analyst

AI-powered Resume Analyzer, ATS scorer, Job Matcher and Skill-Gap Assistant.

## Implementation status

The repository now contains the **full project foundation across Phases 0–11**: architecture, authentication foundation, resume parsing, ATS analysis, job APIs, matching, skill-gap/recommendations, admin APIs, AI provider integration, Redis/Celery, PostgreSQL/pgvector migration, Docker and CI. Some production integrations such as managed S3 storage, real job-source ingestion and advanced learning-to-rank remain deployment/configuration work rather than fake placeholders.

## Features

- Modern responsive Resume AI dashboard
- PDF and DOCX resume upload/parsing
- JWT authentication with Argon2 password hashing
- Resume skill and section analysis
- ATS-style scoring with explainable factors
- Optional OpenAI-powered structured analysis
- Safe deterministic AI fallback when no API key is configured
- Job records and hybrid skill/keyword matching foundation
- Skill-gap analysis
- Job, skill and career recommendations
- Protected admin dashboard endpoints
- PostgreSQL + pgvector baseline migration
- Redis + Celery worker foundation
- Docker Compose local stack
- GitHub Actions CI

## Stack

- Next.js 14 + React + TypeScript
- FastAPI + Python 3.12
- PostgreSQL 16 + pgvector
- SQLAlchemy 2
- Redis + Celery
- PyMuPDF + python-docx
- OpenAI-compatible AI provider layer
- Docker
- GitHub Actions

## Run locally

### Docker

1. Copy `.env.example` to `.env`.
2. Optionally set `OPENAI_API_KEY` for LLM analysis.
3. Run:

```bash
docker compose up --build
```

Frontend: `http://localhost:3000`

API: `http://localhost:8000`

API docs: `http://localhost:8000/docs`

### Without AI provider

The analyzer still works using deterministic skill, section and ATS heuristics. Configure an AI provider key when you want deeper semantic analysis.

## Production checklist

Before public launch, configure a strong `SECRET_KEY`, HTTPS, managed PostgreSQL/Redis, private object storage, malware scanning, rate limits, structured logging, monitoring, backups, secret management, email verification/reset delivery, real job-source integrations subject to their terms, and a full E2E/security/load test suite.

## Documentation

- [Architecture & Implementation Plan](docs/architecture/implementation-plan.md)

## Repository

urlGitHub repositoryhttps://github.com/lithish966-blip/resume-ai-analyst
