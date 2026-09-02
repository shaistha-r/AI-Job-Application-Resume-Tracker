from datetime import datetime

from flask import Blueprint, render_template
from flask_login import login_required, current_user

from models import db, Job, Application, Resume, Reminder


dashboard_bp = Blueprint(
    "dashboard",
    __name__
)


@dashboard_bp.get("/")
@login_required
def index():

    # Current time
    now = datetime.now()

    # -------------------------------------------------
    # JOBS
    # -------------------------------------------------

    jobs = db.session.scalars(
        db.select(Job)
        .where(Job.user_id == current_user.id)
    ).all()

    # -------------------------------------------------
    # APPLICATIONS
    # -------------------------------------------------

    applications = db.session.scalars(
        db.select(Application)
        .where(Application.user_id == current_user.id)
        .order_by(Application.updated_at.desc())
    ).all()

    # -------------------------------------------------
    # RESUMES
    # -------------------------------------------------

    resumes = db.session.scalars(
        db.select(Resume)
        .where(Resume.user_id == current_user.id)
    ).all()

    # -------------------------------------------------
    # EXPIRE OLD REMINDERS
    # -------------------------------------------------

    expired_reminders = db.session.scalars(
        db.select(Reminder).where(
            Reminder.user_id == current_user.id,
            Reminder.completed.is_(False),
            Reminder.due_at < now
        )
    ).all()

    for reminder in expired_reminders:
        reminder.completed = True

    db.session.commit()

    # -------------------------------------------------
    # UPCOMING REMINDERS
    # -------------------------------------------------

    upcoming = db.session.scalars(
        db.select(Reminder)
        .where(
            Reminder.user_id == current_user.id,
            Reminder.completed.is_(False),
            Reminder.due_at >= now
        )
        .order_by(Reminder.due_at)
        .limit(5)
    ).all()

    # -------------------------------------------------
    # APPLICATION STATUS COUNTS
    # -------------------------------------------------

    statuses = [
        "Applied",
        "Assessment",
        "Interview",
        "Offer",
        "Rejected",
        "Withdrawn"
    ]

    status_counts = {}

    for status in statuses:
        status_counts[status] = sum(
            1
            for application in applications
            if application.status == status
        )

    # -------------------------------------------------
    # INTERVIEWS & OFFERS
    # -------------------------------------------------

    interviews = status_counts.get("Interview", 0)
    offers = status_counts.get("Offer", 0)

    # -------------------------------------------------
    # RESPONSE RATE
    # -------------------------------------------------

    total_applications = len(applications)

    response_count = sum(
        1
        for application in applications
        if application.status != "Applied"
    )

    if total_applications > 0:
        response_rate = round(
            (response_count / total_applications) * 100,
            1
        )
    else:
        response_rate = 0

    # -------------------------------------------------
    # DASHBOARD
    # -------------------------------------------------

    return render_template(
        "dashboard/dashboard.html",
        jobs=jobs,
        applications=applications,
        resumes=resumes,
        upcoming=upcoming,
        status_counts=status_counts,
        interviews=interviews,
        offers=offers,
        response_rate=response_rate
    )