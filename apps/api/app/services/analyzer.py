import re
from collections import Counter

SKILLS = [
    "python", "java", "javascript", "typescript", "react", "next.js", "node.js",
    "fastapi", "django", "flask", "sql", "postgresql", "mysql", "mongodb", "redis",
    "docker", "kubernetes", "aws", "azure", "gcp", "git", "github", "excel",
    "power bi", "tableau", "machine learning", "deep learning", "nlp", "pandas",
    "numpy", "scikit-learn", "tensorflow", "pytorch", "figma", "html", "css"
]


def extract_skills(text: str) -> list[str]:
    lower = text.lower()
    return sorted({skill for skill in SKILLS if skill in lower})


def analyze_resume(text: str) -> dict:
    skills = extract_skills(text)
    lower = text.lower()
    sections = {
        "summary": any(x in lower for x in ["summary", "profile", "objective"]),
        "experience": any(x in lower for x in ["experience", "employment", "work history"]),
        "education": "education" in lower,
        "projects": "projects" in lower,
        "certifications": "certification" in lower,
    }
    section_score = sum(sections.values()) / len(sections) * 100
    achievement_count = len(re.findall(r"\b(?:increased|reduced|improved|saved|generated|delivered|achieved)\b", lower))
    keyword_score = min(100, len(skills) * 8)
    achievement_score = min(100, achievement_count * 20)
    ats = round(section_score * .35 + keyword_score * .40 + achievement_score * .25, 1)
    missing = [name for name, present in sections.items() if not present]
    strengths = [f"Detected {len(skills)} relevant skills" if skills else "No standard technical skills detected"]
    if achievement_count:
        strengths.append(f"Found {achievement_count} quantified/action-oriented achievement statements")
    recommendations = [f"Add a {x} section" for x in missing]
    if not achievement_count:
        recommendations.append("Rewrite experience bullets with measurable outcomes")
    return {
        "ats_score": ats,
        "keyword_score": round(keyword_score, 1),
        "section_score": round(section_score, 1),
        "achievement_score": round(achievement_score, 1),
        "skills": skills,
        "sections": sections,
        "strengths": strengths,
        "weaknesses": missing,
        "recommendations": recommendations,
    }


def match_job(resume_text: str, required_skills: list[str], description: str) -> dict:
    resume_skills = set(extract_skills(resume_text))
    required = {s.lower().strip() for s in required_skills}
    matched = sorted(resume_skills & required)
    missing = sorted(required - resume_skills)
    skill_score = 100.0 if not required else round(len(matched) / len(required) * 100, 1)
    # Lightweight semantic proxy until the embedding service is configured.
    resume_words = set(re.findall(r"[a-z0-9+#.-]{3,}", resume_text.lower()))
    job_words = set(re.findall(r"[a-z0-9+#.-]{3,}", description.lower()))
    overlap = len(resume_words & job_words) / max(1, len(job_words))
    semantic_score = round(min(100, overlap * 100), 1)
    overall = round(skill_score * .65 + semantic_score * .35, 1)
    return {"overall_score": overall, "skill_score": skill_score, "semantic_score": semantic_score, "matched_skills": matched, "missing_skills": missing}
