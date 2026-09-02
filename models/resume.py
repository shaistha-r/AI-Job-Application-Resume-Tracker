from datetime import datetime, timezone
from . import db

class Resume(db.Model):
    __tablename__ = "resumes"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    filename = db.Column(db.String(255), nullable=False)
    version_name = db.Column(db.String(120), nullable=False)
    extracted_text = db.Column(db.Text, default="", nullable=False)
    uploaded_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    user = db.relationship("User", back_populates="resumes")
    applications = db.relationship("Application", back_populates="resume")
    analyses = db.relationship("AIAnalysis", back_populates="resume", cascade="all, delete-orphan")
