from sqlalchemy import create_engine, StaticPool, text
from sqlalchemy.orm import sessionmaker

from models import Todos, Users
from database import Base

from main import app

from fastapi.testclient import TestClient

import pytest

from routers.auth import bcrypt_context


SQLALCHEMY_DATABASE_URL = 'sqlite:///./testdb.db'

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    return {'username': 'fatih', 'id': 1,  'user_id': 1, 'role': 'admin'}


client = TestClient(app)

@pytest.fixture
def test_todo():
    todo = Todos(
        title='Learn to code',
        description='Need to learn everyday!',
        priority=5,
        completed=False,
        user_id=1
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo

    with engine.connect() as connection:
       connection.execute(text("DELETE FROM todos;"))
       connection.commit()


@pytest.fixture
def test_user():
    user = Users(
        username="fatih",
        email="example@email.com",
        first_name="Fatih",
        last_name="Aydin",
        hashed_password=bcrypt_context.hash("mypassword"),
        role="admin",
        phone_number="+909999999999"
    )
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()