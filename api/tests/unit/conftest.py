from main import app,db
import pytest

@pytest.fixture(scope="session", autouse=True)
def create_table():
    application = app.app
    with application.app_context():
        db.create_all()
    yield
    with application.app_context():
        db.drop_all()
