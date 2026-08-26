# Resume AI Analyst — Architecture & Implementation Plan

## 1. Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| Frontend | Next.js + TypeScript | Production web application |
| UI | Tailwind CSS + shadcn/ui | Responsive UI system |
| State | TanStack Query | Server-state and caching |
| Forms | React Hook Form + Zod | Form handling and validation |
| Backend | FastAPI + Python | REST API and application services |
| Database | PostgreSQL | Primary relational data store |
| ORM | SQLAlchemy 2 + Alembic | Persistence and migrations |
| Authentication | JWT + HTTP-only cookies | Session/authentication security |
| Password hashing | Argon2id | Password protection |
| File storage | S3-compatible object storage | Private resume documents |
| PDF parsing | PyMuPDF | PDF text extraction |
| DOCX parsing | python-docx | Word document extraction |
| AI | Provider-agnostic LLM abstraction | Resume analysis and recommendations |
| Embeddings | Embedding model abstraction | Semantic matching |
| Vector search | pgvector | Resume/job similarity |
| Background jobs | Celery + Redis | Async processing |
| Testing | Pytest + Vitest + Playwright | Unit/integration/E2E tests |
| CI/CD | GitHub Actions | Automated validation/deployment |
| Runtime | Docker | Reproducible environments |

## 2. Architecture

```text
                         User
                          |
                          v
                   Next.js Web App
                          |
                         HTTPS
                          v
                     FastAPI API
                    /           \
                   v             v
             PostgreSQL        Redis
             + pgvector          |
                   |              v
                   |        Celery Workers
                   |        /      |      \
                   |       v       v       v
                   |    Parser     AI   Embeddings
                   |       |        |       |
                   |       +--------+-------+
                   |                |
                   v                v
              Resume Data       AI Provider
                   ^
                   |
              S3-compatible Storage
```

Heavy parsing, AI analysis, embedding generation and matching are asynchronous jobs. The API creates a job and returns a job ID instead of blocking the request.

## 3. Folder Structure

```text
resume-ai-analyst/
├── apps/
│   ├── web/
│   │   ├── app/
│   │   │   ├── (auth)/
│   │   │   ├── dashboard/
│   │   │   ├── resume/
│   │   │   ├── jobs/
│   │   │   ├── recommendations/
│   │   │   ├── skill-gap/
│   │   │   └── admin/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── lib/
│   │   ├── services/
│   │   ├── types/
│   │   └── tests/
│   └── api/
│       ├── app/
│       │   ├── api/
│       │   ├── core/
│       │   ├── models/
│       │   ├── schemas/
│       │   ├── services/
│       │   ├── repositories/
│       │   ├── workers/
│       │   ├── ai/
│       │   ├── parsers/
│       │   └── main.py
│       └── tests/
├── packages/
│   ├── shared-types/
│   └── config/
├── database/
│   ├── migrations/
│   └── seeds/
├── infrastructure/
│   ├── docker/
│   ├── nginx/
│   └── deployment/
├── docs/
│   ├── architecture/
│   ├── api/
│   └── security/
├── scripts/
├── .github/
│   └── workflows/
├── .env.example
├── docker-compose.yml
├── README.md
└── LICENSE
```

## 4. Database Schema

### users

`id UUID PK`, `email UNIQUE`, `password_hash`, `full_name`, `role`, `is_active`, `email_verified`, `created_at`, `updated_at`.

### resumes

`id UUID PK`, `user_id FK`, `file_name`, `file_type`, `storage_key`, `file_size`, `raw_text`, `status`, `created_at`, `updated_at`.

### resume_profiles

`id UUID PK`, `resume_id FK`, `summary`, `years_experience`, `education JSONB`, `experience JSONB`, `projects JSONB`, `certifications JSONB`, `languages JSONB`, `contact JSONB`.

### skills

`id UUID PK`, `name UNIQUE`, `category`, `normalized_name`.

### resume_skills

`resume_id FK`, `skill_id FK`, `proficiency`, `years_experience`, `confidence`.

### jobs

`id UUID PK`, `external_id`, `source`, `title`, `company`, `description`, `location`, `employment_type`, `experience_level`, `salary_min`, `salary_max`, `currency`, `url`, `posted_at`, `expires_at`, `created_at`.

### job_skills

`job_id FK`, `skill_id FK`, `importance`, `required`.

### resume_analysis

`id UUID PK`, `resume_id FK`, `overall_score`, `ats_score`, `content_score`, `format_score`, `keyword_score`, `experience_score`, `education_score`, `summary JSONB`, `strengths JSONB`, `weaknesses JSONB`, `recommendations JSONB`, `created_at`.

### job_matches

`id UUID PK`, `resume_id FK`, `job_id FK`, `overall_score`, `skill_score`, `semantic_score`, `experience_score`, `location_score`, `explanation JSONB`, `created_at`.

### skill_gaps

`id UUID PK`, `resume_id FK`, `job_id FK`, `skill_id FK`, `importance`, `gap_level`, `recommendation`.

### embeddings

`id UUID PK`, `entity_type`, `entity_id`, `embedding VECTOR`, `model`, `created_at`.

## 5. API Endpoints

### Authentication

```text
POST /api/v1/auth/register
POST /api/v1/auth/login
POST /api/v1/auth/logout
POST /api/v1/auth/refresh
POST /api/v1/auth/forgot-password
POST /api/v1/auth/reset-password
GET  /api/v1/auth/me
```

### Resume

```text
POST   /api/v1/resumes/upload
GET    /api/v1/resumes
GET    /api/v1/resumes/{resume_id}
DELETE /api/v1/resumes/{resume_id}
POST   /api/v1/resumes/{resume_id}/analyze
GET    /api/v1/resumes/{resume_id}/analysis
```

### ATS

```text
POST /api/v1/ats/analyze
GET  /api/v1/ats/{analysis_id}
```

### Jobs

```text
GET  /api/v1/jobs
GET  /api/v1/jobs/{job_id}
POST /api/v1/jobs/search
POST /api/v1/jobs/{job_id}/save
DELETE /api/v1/jobs/{job_id}/save
```

### Matching

```text
GET  /api/v1/matches
GET  /api/v1/matches/{job_id}
POST /api/v1/matches/generate
```

### Skill Gap

```text
GET /api/v1/skill-gaps
GET /api/v1/skill-gaps/{job_id}
```

### Recommendations

```text
GET /api/v1/recommendations/jobs
GET /api/v1/recommendations/skills
GET /api/v1/recommendations/careers
```

### Profile

```text
GET /api/v1/profile
PUT /api/v1/profile
PUT /api/v1/preferences
```

### Admin

```text
GET    /api/v1/admin/dashboard
GET    /api/v1/admin/users
GET    /api/v1/admin/resumes
GET    /api/v1/admin/jobs
GET    /api/v1/admin/analytics
DELETE /api/v1/admin/users/{user_id}
```

## 6. AI Architecture

The AI layer is modular rather than a single prompt.

```text
Resume PDF/DOCX
      |
      v
Document Parser
      |
      v
Text Cleaning
      |
      v
Section Detection
      |
      v
Structured Resume Extraction
      |
      +------> Skill Extraction
      +------> Experience Extraction
      +------> Education Extraction
      |
      v
Embedding Generation
      |
      +--------------------+
      |                    |
      v                    v
ATS Analysis          Job Matching
      |                    |
      v                    v
Recommendations      Skill Gap Analysis
```

AI outputs should use schema-constrained structured data. Resume and job text are untrusted input and must never be allowed to override system instructions or invoke unauthorized tools.

## 7. ATS Scoring

Initial configurable scoring model:

- Keyword Match: 25%
- Resume Structure: 20%
- Experience Relevance: 15%
- Skills: 15%
- Education: 10%
- Achievement Quality: 10%
- Formatting: 5%

The score is an estimate and must not be represented as the exact score of a specific employer ATS.

## 8. Job Matching Algorithm

Use hybrid ranking instead of relying only on an LLM.

### Stage 1 — Hard filters

Filter by location, work authorization, employment type, experience range, salary requirements and required qualifications where available.

### Stage 2 — Skill matching

Compare normalized resume skills with required and preferred job skills. Related skills can receive partial semantic credit.

### Stage 3 — Semantic matching

Generate embeddings for the candidate profile and job description and calculate vector similarity with pgvector.

### Stage 4 — Experience matching

Compare required experience and candidate experience.

### Stage 5 — Final ranking

Initial configurable weighting:

- Semantic Similarity: 30%
- Skill Match: 25%
- Required Skill Match: 15%
- Experience Match: 10%
- Job Preference Match: 10%
- Location Match: 5%
- Education/Certification Match: 5%

Every match should provide an explanation showing matched skills, missing skills and important reasons behind the score.

## 9. Skill-Gap Analysis

For each target job, calculate the set difference between required job skills and candidate skills, then rank gaps by importance. The AI layer can generate learning recommendations, but the underlying missing-skill calculation should remain deterministic and auditable.

## 10. Job Recommendations

Initial recommendation ranking should combine match score and explicit user preferences. Track views, saves, applications, dismissals, searches, preferred roles, locations and salary ranges. Once sufficient interaction data exists, a learning-to-rank model can be introduced.

## 11. Admin Dashboard

Provide:

- User management
- Resume analytics
- Job analytics
- AI request monitoring
- Token/cost tracking
- Processing failures
- System health
- Audit logs

## 12. Security

### Authentication

- Argon2id password hashing
- Short-lived access tokens
- HTTP-only secure cookies
- Refresh-token rotation
- Email verification
- Password reset
- Role-based authorization

### File security

- MIME and extension validation
- File-size limits
- Malware scanning
- Random storage keys
- Private object storage
- Signed download URLs
- No public resume URLs

### API security

- HTTPS
- Strict CORS
- CSRF protection where applicable
- Rate limiting
- Input validation
- Parameterized database access
- Security headers
- Request-size limits
- Audit logging

### AI security

- Treat all uploaded text as untrusted
- Defend against prompt injection
- Separate system instructions from document content
- Do not expose secrets to the model
- Restrict tool access
- Validate structured AI output before persistence

## 13. Deployment

```text
Internet
   |
Cloudflare/CDN
   |
Next.js
   |
FastAPI
 / | \
PostgreSQL Redis S3
          |
       Celery
          |
     AI/Parsing Workers
```

Use Docker for reproducible builds, GitHub Actions for CI/CD, managed PostgreSQL and Redis, private S3-compatible storage, centralized logging and error monitoring.

## 14. Development Phases

### Phase 0 — Foundation

- Repository and monorepo structure
- Docker environment
- PostgreSQL
- Redis
- Migrations
- Frontend/backend foundations
- CI

### Phase 1 — Authentication

- Registration/login/logout
- Password security
- JWT/session handling
- Refresh tokens
- Verification/reset flows
- Role authorization

### Phase 2 — Resume Parsing

- PDF/DOCX upload
- Validation
- Private storage
- Text extraction
- Text normalization
- Section detection
- Structured profile extraction

### Phase 3 — AI Resume Analyzer

- Skill extraction
- Experience extraction
- Resume quality analysis
- Strengths/weaknesses
- Recommendations
- Keyword analysis

### Phase 4 — ATS Engine

- ATS scoring
- Keyword checks
- Section checks
- Formatting checks
- Job-specific scoring

### Phase 5 — Job Database

- Job ingestion
- Normalization
- Deduplication
- Skill extraction
- Categorization
- Expiration handling

### Phase 6 — Job Matching

- Hard filtering
- Skill matching
- Embeddings
- Experience matching
- Preference matching
- Ranking explanations

### Phase 7 — Skill Gap

- Missing skills
- Required/preferred distinction
- Gap priority
- Learning recommendations

### Phase 8 — Recommendations

- Recommended jobs
- Recommended skills
- Career-path recommendations
- Personalized ranking

### Phase 9 — Admin

- User management
- Resume/job analytics
- AI monitoring
- Audit logs

### Phase 10 — Production Hardening

- Security audit
- Rate limiting
- Reliability testing
- Database indexing
- Caching
- Logging
- Monitoring
- Backups
- Data deletion/privacy controls
- Load testing
- E2E testing

### Phase 11 — Deployment

- CI/CD
- Staging
- Production
- Monitoring
- Rollback strategy

## 15. Implementation Rules

1. Do not commit API keys or secrets.
2. Keep AI providers behind interfaces.
3. Use async workers for expensive processing.
4. Validate every external input.
5. Make scoring explainable and configurable.
6. Keep resume files private.
7. Add tests alongside production features.
8. Use migrations for all database changes.
9. Keep frontend and backend independently deployable.
10. Do not claim an ATS score is an exact prediction of a specific employer's ATS.
