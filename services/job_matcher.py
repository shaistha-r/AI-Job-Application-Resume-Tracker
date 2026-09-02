import re
from services.ai_analyzer import SKILLS

REQUIRED_MARKERS = ("required", "must have", "must-have", "requirements", "qualifications", "essential")
PREFERRED_MARKERS = ("preferred", "nice to have", "bonus", "good to have")

def _skills(text):
    lower = text.lower()
    found = []
    for skill in SKILLS:
        if re.search(r"(?<![a-z0-9])" + re.escape(skill) + r"(?![a-z0-9])", lower):
            found.append(skill.title() if skill not in {"c", "c++", "sql", "aws", "gcp"} else skill.upper())
    return found

def _normalize(items):
    aliases = {"javascript":"JavaScript", "js":"JavaScript", "rest":"REST API", "rest api":"REST API", "node.js":"Node.js", "c++":"C++"}
    return [aliases.get(x.lower(), x) for x in items]

def match_resume_to_job(resume_text, job_text):
    resume_skills = set(_normalize(_skills(resume_text)))
    job_skills = _normalize(_skills(job_text))
    required = []
    preferred = []
    lower = job_text.lower()
    for skill in job_skills:
        pos = lower.find(skill.lower())
        window = lower[max(0,pos-100):pos+100] if pos >= 0 else lower
        if any(m in window for m in PREFERRED_MARKERS):
            preferred.append(skill)
        else:
            required.append(skill)
    required = list(dict.fromkeys(required))
    preferred = [s for s in dict.fromkeys(preferred) if s not in required]
    if not required and job_skills:
        required = list(dict.fromkeys(job_skills))
    matched_required = [s for s in required if s in resume_skills]
    matched_preferred = [s for s in preferred if s in resume_skills]
    missing = [s for s in required + preferred if s not in resume_skills]
    required_score = len(matched_required)/len(required) if required else 1
    preferred_score = len(matched_preferred)/len(preferred) if preferred else 1
    project_score = 1 if any(k in resume_text.lower() for k in ["project", "experience", "internship"]) else 0.5
    keyword_overlap = len(set(_skills(resume_text)) & set(_skills(job_text))) / max(1, len(set(_skills(job_text))))
    score = round((required_score*.50 + preferred_score*.20 + project_score*.15 + keyword_overlap*.15)*100, 1)
    return {"score":score,"matched_skills":list(dict.fromkeys(matched_required+matched_preferred)),"missing_skills":missing,"required_skills":required,"preferred_skills":preferred,"breakdown":{"required_skills":round(required_score*100,1),"preferred_skills":round(preferred_score*100,1),"project_experience":round(project_score*100,1),"keyword_relevance":round(keyword_overlap*100,1)}}

def build_skill_gap(missing):
    priority = []
    for skill in missing:
        priority.append({"skill":skill,"priority":"High" if skill in missing[:3] else "Medium","learning":"Learn the fundamentals, build a small project, then add truthful evidence to your resume."})
    return priority
