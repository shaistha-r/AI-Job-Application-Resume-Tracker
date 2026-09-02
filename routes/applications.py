from datetime import datetime, timezone

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from models import db, Job, Resume, Application, Reminder


applications_bp = Blueprint(
    "applications",
    __name__,
    url_prefix="/applications"
)

STATUSES = [
    "Applied",
    "Assessment",
    "Interview",
    "Offer",
    "Rejected",
    "Withdrawn"
]


@applications_bp.get("/")
@login_required
def list_applications():

    applications = db.session.scalars(
        db.select(Application)
        .where(Application.user_id == current_user.id)
        .order_by(Application.updated_at.desc())
    ).all()

    return render_template(
        "applications/applications.html",
        applications=applications,
        statuses=STATUSES
    )


@applications_bp.post("/create/<int:job_id>")
@login_required
def create(job_id):

    job = db.session.scalar(
        db.select(Job).where(
            Job.id == job_id,
            Job.user_id == current_user.id
        )
    )

    if not job:
        flash("Job not found.", "error")
        return redirect(url_for("jobs.list_jobs"))

    existing = db.session.scalar(
        db.select(Application).where(
            Application.job_id == job.id,
            Application.user_id == current_user.id
        )
    )

    if existing:
        flash("You already have an application for this job.", "error")
        return redirect(url_for("jobs.detail", job_id=job.id))

    resume_id = request.form.get("resume_id", type=int)

    resume = None

    if resume_id:
        resume = db.session.scalar(
            db.select(Resume).where(
                Resume.id == resume_id,
                Resume.user_id == current_user.id
            )
        )

    application = Application(
        user_id=current_user.id,
        job_id=job.id,
        resume_id=resume.id if resume else None,
        status=request.form.get("status", "Applied"),
        notes=request.form.get("notes", "").strip()
    )

    db.session.add(application)

    job.status = application.status

    db.session.flush()

    # Job deadline reminder
    if job.deadline:
        from services.reminder_service import sync_job_deadline_reminder

        sync_job_deadline_reminder(job)

    db.session.commit()

    flash("Application created.", "success")

    return redirect(
        url_for("applications.list_applications")
    )


@applications_bp.post("/<int:application_id>/status")
@login_required
def update_status(application_id):

    application = db.session.scalar(
        db.select(Application).where(
            Application.id == application_id,
            Application.user_id == current_user.id
        )
    )

    if not application:
        flash("Application not found.", "error")

        return redirect(
            url_for("applications.list_applications")
        )

    status = request.form.get("status")

    if status in STATUSES:

        application.status = status
        application.job.status = status

        # -------------------------------------------------
        # INTERVIEW REMINDER
        # -------------------------------------------------

        interview_date = request.form.get("interview_date")

        if interview_date:

            application.interview_date = datetime.strptime(
                interview_date,
                "%Y-%m-%dT%H:%M"
            )

            # Look for an existing interview reminder
            reminder = db.session.scalar(
                db.select(Reminder).where(
                    Reminder.user_id == current_user.id,
                    Reminder.application_id == application.id,
                    Reminder.type == "Interview"
                )
            )

            if reminder:

                # UPDATE existing reminder
                reminder.due_at = application.interview_date
                reminder.completed = False

            else:

                # CREATE reminder only if one doesn't exist
                reminder = Reminder(
                    user_id=current_user.id,
                    application_id=application.id,
                    job_id=application.job_id,
                    type="Interview",
                    due_at=application.interview_date,
                    completed=False
                )

                db.session.add(reminder)

        db.session.commit()

        flash("Application updated.", "success")

    return redirect(
        url_for("applications.list_applications")
    )