from pathlib import Path
from flask import Flask
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from config import Config
from models import db, User

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Please log in to continue."
csrf = CSRFProtect()

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)
    Path(app.config["UPLOAD_FOLDER"]).mkdir(parents=True, exist_ok=True)
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.jobs import jobs_bp
    from routes.applications import applications_bp
    from routes.resumes import resumes_bp
    from routes.ai import ai_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(jobs_bp)
    app.register_blueprint(applications_bp)
    app.register_blueprint(resumes_bp)
    app.register_blueprint(ai_bp)

    @app.context_processor
    def inject_globals():
        return {"app_name": "AI Job & Resume Tracker"}

    @app.errorhandler(413)
    def too_large(_):
        from flask import flash, redirect, url_for
        flash("File is too large. Maximum size is 5 MB.", "error")
        return redirect(url_for("resumes.upload"))

    with app.app_context():
        db.create_all()
    return app

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
