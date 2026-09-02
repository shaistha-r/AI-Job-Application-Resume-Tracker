import json
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Resume, Job, AIAnalysis
from services.ai_analyzer import analyze_resume, generate_job_feedback
from services.job_matcher import match_resume_to_job, build_skill_gap

ai_bp = Blueprint("ai", __name__, url_prefix="/ai")

def owned_resume(resume_id):
    return db.session.scalar(db.select(Resume).where(Resume.id == resume_id, Resume.user_id == current_user.id))

def owned_job(job_id):
    return db.session.scalar(db.select(Job).where(Job.id == job_id, Job.user_id == current_user.id))

@ai_bp.get("/analyze-resume/<int:resume_id>")
@login_required
def analyze_resume_route(resume_id):
    resume = owned_resume(resume_id)
    if not resume:
        flash("Resume not found.", "error")
        return redirect(url_for("resumes.list_resumes"))
    data = analyze_resume(resume.extracted_text)
    return render_template("ai/analysis.html", resume=resume, data=data, job=None, match=None)

@ai_bp.get("/match/<int:job_id>/<int:resume_id>")
@login_required
def match(job_id, resume_id):
    job = owned_job(job_id)
    resume = owned_resume(resume_id)
    if not job or not resume:
        flash("Job or resume not found.", "error")
        return redirect(url_for("dashboard.index"))
    result = match_resume_to_job(resume.extracted_text, job.description)
    feedback = generate_job_feedback(resume.extracted_text, job.description, result)
    analysis = AIAnalysis(user_id=current_user.id, resume_id=resume.id, job_id=job.id, score=result["score"], matched_skills=json.dumps(result["matched_skills"]), missing_skills=json.dumps(result["missing_skills"]), feedback=feedback)
    db.session.add(analysis)
    db.session.commit()
    return render_template("ai/analysis.html", resume=resume, job=job, match=result, data=analyze_resume(resume.extracted_text), analysis=analysis)

@ai_bp.get("/skill-gap/<int:job_id>/<int:resume_id>")
@login_required
def skill_gap(job_id, resume_id):
    job = owned_job(job_id)
    resume = owned_resume(resume_id)
    if not job or not resume:
        flash("Job or resume not found.", "error")
        return redirect(url_for("dashboard.index"))
    result = match_resume_to_job(resume.extracted_text, job.description)
    gap = build_skill_gap(result["missing_skills"])
    return render_template("ai/skill_gap.html", job=job, resume=resume, gap=gap, match=result)
