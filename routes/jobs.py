from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from sqlalchemy import or_
from models import db, Job, Application, Reminder, Resume
from services.reminder_service import sync_job_deadline_reminder

jobs_bp = Blueprint("jobs", __name__, url_prefix="/jobs")
STATUSES = ["Saved", "Applied", "Assessment", "Interview", "Offer", "Rejected", "Withdrawn"]

def get_user_job(job_id):
    return db.session.scalar(db.select(Job).where(Job.id == job_id, Job.user_id == current_user.id))

@jobs_bp.get("/")
@login_required
def list_jobs():
    q = request.args.get("q", "").strip()
    status = request.args.get("status", "").strip()
    stmt = db.select(Job).where(Job.user_id == current_user.id).order_by(Job.created_at.desc())
    if q:
        stmt = stmt.where(or_(Job.company.ilike(f"%{q}%"), Job.title.ilike(f"%{q}%")))
    if status:
        stmt = stmt.where(Job.status == status)
    jobs = db.session.scalars(stmt).all()
    return render_template("jobs/jobs.html", jobs=jobs, statuses=STATUSES, q=q, selected_status=status)

@jobs_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_job():
    if request.method == "POST":
        company = request.form.get("company", "").strip()
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        if not company or not title or not description:
            flash("Company, title and description are required.", "error")
            return render_template("jobs/add_job.html", job=None)
        deadline = None
        if request.form.get("deadline"):
            deadline = datetime.strptime(request.form["deadline"], "%Y-%m-%d").date()
        job = Job(user_id=current_user.id, company=company, title=title, description=description, url=request.form.get("url", "").strip(), location=request.form.get("location", "").strip(), salary=request.form.get("salary", "").strip(), deadline=deadline, status=request.form.get("status") or "Saved")
        db.session.add(job)
        db.session.flush()
        sync_job_deadline_reminder(job)
        db.session.commit()
        flash("Job saved.", "success")
        return redirect(url_for("jobs.detail", job_id=job.id))
    return render_template("jobs/add_job.html", job=None, statuses=STATUSES)

@jobs_bp.route("/<int:job_id>/edit", methods=["GET", "POST"])
@login_required
def edit_job(job_id):
    job = get_user_job(job_id)
    if not job:
        flash("Job not found.", "error")
        return redirect(url_for("jobs.list_jobs"))
    if request.method == "POST":
        job.company = request.form.get("company", "").strip()
        job.title = request.form.get("title", "").strip()
        job.description = request.form.get("description", "").strip()
        job.url = request.form.get("url", "").strip()
        job.location = request.form.get("location", "").strip()
        job.salary = request.form.get("salary", "").strip()
        job.status = request.form.get("status", "Saved")
        job.deadline = datetime.strptime(request.form["deadline"], "%Y-%m-%d").date() if request.form.get("deadline") else None
        sync_job_deadline_reminder(job)
        db.session.commit()
        flash("Job updated.", "success")
        return redirect(url_for("jobs.detail", job_id=job.id))
    return render_template("jobs/add_job.html", job=job, statuses=STATUSES)

@jobs_bp.post("/<int:job_id>/delete")
@login_required
def delete_job(job_id):
    job = get_user_job(job_id)
    if job:
        db.session.delete(job)
        db.session.commit()
        flash("Job deleted.", "success")
    return redirect(url_for("jobs.list_jobs"))

@jobs_bp.get("/<int:job_id>")
@login_required
def detail(job_id):
    job = get_user_job(job_id)
    if not job:
        flash("Job not found.", "error")
        return redirect(url_for("jobs.list_jobs"))
    resumes = db.session.scalars(db.select(Resume).where(Resume.user_id == current_user.id).order_by(Resume.uploaded_at.desc())).all()
    application = db.session.scalar(db.select(Application).where(Application.job_id == job.id, Application.user_id == current_user.id))
    return render_template("jobs/job_detail.html", job=job, resumes=resumes, application=application)
