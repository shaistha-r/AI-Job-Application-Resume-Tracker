from datetime import datetime, timezone
from . import db

class Application(db.Model):
    __tablename__ = "applications"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"), nullable=False)
    resume_id = db.Column(db.Integer, db.ForeignKey("resumes.id"), nullable=True)
    status = db.Column(db.String(30), default="Applied", nullable=False)
    applied_at = db.Column(db.Date, default=lambda: datetime.now(timezone.utc).date())
    interview_date = db.Column(db.DateTime)
    notes = db.Column(db.Text)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    user = db.relationship("User", back_populates="applications")
    job = db.relationship("Job", back_populates="applications")
    resume = db.relationship("Resume", back_populates="applications")
    reminders = db.relationship("Reminder", back_populates="application", cascade="all, delete-orphan")

    __table_args__ = (db.UniqueConstraint("user_id", "job_id", name="uq_user_job_application"),)
