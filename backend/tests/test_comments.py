import pytest
from app import create_app
from app.database import db

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.test_client() as client:
        with app.app_context():
            db.drop_all()     # 👈 ADD THIS
            db.create_all()   # 👈 AND THIS
        yield client



def test_create_comment(client):
    response = client.post("/comments", json={"text": "Hello World"})
    assert response.status_code == 201
    assert response.json["text"] == "Hello World"


def test_get_comments(client):
    client.post("/comments", json={"text": "First"})
    response = client.get("/comments")
    assert response.status_code == 200
    assert len(response.json) == 1


def test_update_comment(client):
    post = client.post("/comments", json={"text": "Old"})
    comment_id = post.json["id"]

    response = client.put(f"/comments/{comment_id}", json={"text": "Updated"})
    assert response.status_code == 200
    assert response.json["text"] == "Updated"


def test_delete_comment(client):
    post = client.post("/comments", json={"text": "To be deleted"})
    comment_id = post.json["id"]

    response = client.delete(f"/comments/{comment_id}")
    assert response.status_code == 200
