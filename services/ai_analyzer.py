import json
import re
from config import Config

SKILLS = [
    "python", "java", "c", "c++", "javascript", "typescript", "html", "css", "react", "angular", "node.js", "flask", "django", "spring", "sql", "mysql", "postgresql", "mongodb", "git", "github", "docker", "kubernetes", "aws", "azure", "gcp", "rest api", "rest", "api testing", "pytest", "selenium", "pandas", "numpy", "opencv", "machine learning", "deep learning", "nlp", "tensorflow", "pytorch", "data analysis", "power bi", "excel", "linux", "fastapi", "firebase"
]

def _fallback(text):
    lower = text.lower()
    found = []
    for skill in SKILLS:
        pattern = r"(?<![a-z0-9])" + re.escape(skill) + r"(?![a-z0-9])"
        if re.search(pattern, lower):
            found.append(skill.title() if skill not in {"c", "c++", "sql", "aws", "gcp", "api"} else skill.upper())
    sections = {"skills": found, "education": [], "projects": [], "experience": [], "keywords": found[:15]}
    for marker in ["b.e", "btech", "b.tech", "bachelor", "master", "mca", "engineering"]:
        if marker in lower:
            sections["education"].append(marker.upper())
    return sections

def analyze_resume(text):
    if not Config.AI_API_KEY:
        result = _fallback(text)
        result["provider"] = "local-fallback"
        return result
    try:
        from openai import OpenAI
        client = OpenAI(api_key=Config.AI_API_KEY)
        schema = {"type":"object","properties":{
            "skills":{"type":"array","items":{"type":"string"}},
            "education":{"type":"array","items":{"type":"string"}},
            "projects":{"type":"array","items":{"type":"string"}},
            "experience":{"type":"array","items":{"type":"string"}},
            "keywords":{"type":"array","items":{"type":"string"}}
        },"required":["skills","education","projects","experience","keywords"],"additionalProperties":False}
        response = client.responses.create(
            model=Config.AI_MODEL,
            instructions="Extract only information explicitly supported by the resume. Return concise structured data. Never invent facts.",
            input=text[:50000],
            text={"format":{"type":"json_schema","name":"resume_analysis","schema":schema,"strict":True}}
        )
        result = json.loads(response.output_text)
        result["provider"] = "openai"
        return result
    except Exception:
        result = _fallback(text)
        result["provider"] = "local-fallback-after-ai-error"
        return result

def generate_job_feedback(resume_text, job_text, match):
    if not Config.AI_API_KEY:
        missing = ", ".join(match["missing_skills"][:5]) or "No major skill gaps detected"
        return f"Focus on demonstrating the required skills in your resume. Priority gap(s): {missing}. Add concrete project evidence and measurable outcomes where truthful."
    try:
        from openai import OpenAI
        client = OpenAI(api_key=Config.AI_API_KEY)
        response = client.responses.create(
            model=Config.AI_MODEL,
            instructions="Give concise, truthful, job-specific resume feedback. Do not guarantee ATS scores or interviews. Do not invent experience.",
            input=f"RESUME:\n{resume_text[:30000]}\n\nJOB:\n{job_text[:30000]}\n\nMATCH RESULT:\n{json.dumps(match)}"
        )
        return response.output_text.strip()
    except Exception:
        return "Use the matched skills prominently, add missing relevant skills only if you genuinely have them, and strengthen project bullets with specific technologies and measurable outcomes."
