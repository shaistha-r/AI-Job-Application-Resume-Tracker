import os
from pathlib import Path
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models import db, Resume
from services.resume_parser import extract_text

resumes_bp = Blueprint("resumes", __name__, url_prefix="/resumes")
ALLOWED = {"pdf", "docx"}

def valid_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED

@resumes_bp.get("/")
@login_required
def list_resumes():
    resumes = db.session.scalars(db.select(Resume).where(Resume.user_id == current_user.id).order_by(Resume.uploaded_at.desc())).all()
    return render_template("resumes/resumes.html", resumes=resumes)

@resumes_bp.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    if request.method == "POST":
        file = request.files.get("resume")
        version_name = request.form.get("version_name", "Resume Version").strip()
        if not file or not file.filename:
            flash("Please choose a resume file.", "error")
            return render_template("resumes/upload.html")
        if not valid_file(file.filename):
            flash("Only PDF and DOCX resumes are supported.", "error")
            return render_template("resumes/upload.html")
        safe_name = secure_filename(file.filename)
        stored_name = f"{current_user.id}_{os.urandom(8).hex()}_{safe_name}"
        path = Path(current_app.config["UPLOAD_FOLDER"]) / stored_name
        file.save(path)
        try:
            text = extract_text(str(path))
        except Exception as exc:
            path.unlink(missing_ok=True)
            flash(f"Could not parse the resume: {exc}", "error")
            return render_template("resumes/upload.html")
        resume = Resume(user_id=current_user.id, filename=stored_name, version_name=version_name or "Resume Version", extracted_text=text)
        db.session.add(resume)
        db.session.commit()
        flash("Resume uploaded and parsed successfully.", "success")
        return redirect(url_for("resumes.list_resumes"))
    return render_template("resumes/upload.html")

@resumes_bp.post("/<int:resume_id>/delete")
@login_required
def delete(resume_id):
    resume = db.session.scalar(db.select(Resume).where(Resume.id == resume_id, Resume.user_id == current_user.id))
    if resume:
        path = Path(current_app.config["UPLOAD_FOLDER"]) / resume.filename
        path.unlink(missing_ok=True)
        db.session.delete(resume)
        db.session.commit()
        flash("Resume deleted.", "success")
    return redirect(url_for("resumes.list_resumes"))
