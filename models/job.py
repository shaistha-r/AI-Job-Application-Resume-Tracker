from datetime import datetime, timezone
from . import db

class Job(db.Model):
    __tablename__ = "jobs"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    company = db.Column(db.String(150), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    url = db.Column(db.String(500))
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(150))
    salary = db.Column(db.String(100))
    deadline = db.Column(db.Date)
    status = db.Column(db.String(30), default="Saved", nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    user = db.relationship("User", back_populates="jobs")
    applications = db.relationship("Application", back_populates="job", cascade="all, delete-orphan")
    analyses = db.relationship("AIAnalysis", back_populates="job", cascade="all, delete-orphan")
    reminders = db.relationship("Reminder", back_populates="job", cascade="all, delete-orphan")
