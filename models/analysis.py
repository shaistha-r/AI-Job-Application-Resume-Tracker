from datetime import datetime, timezone
from . import db

class AIAnalysis(db.Model):
    __tablename__ = "ai_analyses"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    resume_id = db.Column(db.Integer, db.ForeignKey("resumes.id"), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"), nullable=True)
    score = db.Column(db.Float)
    matched_skills = db.Column(db.Text, default="[]", nullable=False)
    missing_skills = db.Column(db.Text, default="[]", nullable=False)
    feedback = db.Column(db.Text, default="", nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    user = db.relationship("User", back_populates="analyses")
    resume = db.relationship("Resume", back_populates="analyses")
    job = db.relationship("Job", back_populates="analyses")
