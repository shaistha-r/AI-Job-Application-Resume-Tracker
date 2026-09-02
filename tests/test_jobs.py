import pytest
from app import create_app
from models import db

@pytest.fixture()
def client(tmp_path):
    app=create_app({"TESTING":True,"WTF_CSRF_ENABLED":False,"SQLALCHEMY_DATABASE_URI":f"sqlite:///{tmp_path/'test.db'}","UPLOAD_FOLDER":str(tmp_path/'uploads'),"SECRET_KEY":"test"})
    with app.test_client() as client:
        with app.app_context(): db.drop_all(); db.create_all()
        client.post('/register',data={"name":"Test","email":"test@example.com","password":"secret1","confirm_password":"secret1"})
        yield client

def test_job_crud(client):
    r=client.post('/jobs/add',data={"company":"Example","title":"Python Intern","description":"Python Flask SQL Git","status":"Saved"},follow_redirects=True)
    assert r.status_code==200 and b"Example" in r.data
    r=client.get('/jobs/')
    assert b"Python Intern" in r.data
