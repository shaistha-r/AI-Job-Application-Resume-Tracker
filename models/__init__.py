from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .job import Job
from .resume import Resume
from .application import Application
from .analysis import AIAnalysis
from .reminder import Reminder

__all__ = ["db", "User", "Job", "Resume", "Application", "AIAnalysis", "Reminder"]
