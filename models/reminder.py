from datetime import datetime, timezone
from . import db

class Reminder(db.Model):
    __tablename__ = "reminders"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    application_id = db.Column(db.Integer, db.ForeignKey("applications.id"), nullable=True)
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"), nullable=True)
    type = db.Column(db.String(50), nullable=False)
    due_at = db.Column(db.DateTime, nullable=False)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    user = db.relationship("User", back_populates="reminders")
    application = db.relationship("Application", back_populates="reminders")
    job = db.relationship("Job", back_populates="reminders")
