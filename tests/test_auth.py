import pytest
from app import create_app
from models import db

@pytest.fixture()
def client(tmp_path):
    app=create_app({"TESTING":True,"WTF_CSRF_ENABLED":False,"SQLALCHEMY_DATABASE_URI":f"sqlite:///{tmp_path/'test.db'}","UPLOAD_FOLDER":str(tmp_path/'uploads'),"SECRET_KEY":"test"})
    with app.test_client() as client:
        with app.app_context(): db.drop_all(); db.create_all()
        yield client

def test_register_and_login(client):
    r=client.post('/register',data={"name":"Test User","email":"test@example.com","password":"secret1","confirm_password":"secret1"},follow_redirects=True)
    assert r.status_code==200
    r=client.post('/logout',follow_redirects=True)
    assert r.status_code==200
    r=client.post('/login',data={"email":"test@example.com","password":"secret1"},follow_redirects=True)
    assert b"Dashboard" in r.data
