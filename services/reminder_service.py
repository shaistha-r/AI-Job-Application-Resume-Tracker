from datetime import datetime, time, timezone
from models import db, Reminder

def sync_job_deadline_reminder(job):
    if not job.deadline:
        return
    due = datetime.combine(job.deadline, time(9,0), tzinfo=timezone.utc)
    existing = db.session.scalar(db.select(Reminder).where(Reminder.user_id==job.user_id, Reminder.job_id==job.id, Reminder.type=="Application Deadline"))
    if existing:
        existing.due_at = due
        existing.completed = False
    else:
        db.session.add(Reminder(user_id=job.user_id, job_id=job.id, type="Application Deadline", due_at=due))
