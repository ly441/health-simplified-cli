
import pytest
from sqlalchemy.orm import Session
from health_cli.db.database import Base, engine, SessionLocal
from health_cli.models.users_entry import User
from health_cli.models.users_entry import (
    create_user,
    get_user_by_id,
    get_user_by_name,
    get_all_users,
    update_user_name,
    delete_user,
)
# Create all tables
Base.metadata.create_all(bind=engine)

# Fixture to create a database session
@pytest.fixture(autouse=True)
def db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.query(User).delete()
        session.commit()
        session.close()

# Fixture to create a test user with a unique email and name
@pytest.fixture
def test_user(db_session, request):
    unique_id = request.node.name
    email = f"test_{unique_id}@example.com"
    name = f"Test User {unique_id}"
    user = User(name=name, email=email)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

# CREATE
def test_create_user(db_session):
    unique_id = "create_user"
    email = f"john.doe_{unique_id}@example.com"
    name = f"John Doe {unique_id}"
    user = create_user(db=db_session, name=name, email=email)
    assert user.id is not None
    assert user.name == name
    assert user.email == email

# READ by user_id
def test_get_user_by_id(db_session, test_user):
    retrieved_user = get_user_by_id(db=db_session, user_id=test_user.id)
    assert retrieved_user is not None
    assert retrieved_user.id == test_user.id
    assert retrieved_user.name == test_user.name
    assert retrieved_user.email == test_user.email

# READ by name
def test_get_user_by_name(db_session, test_user):
    retrieved_user = get_user_by_name(db=db_session, name=test_user.name)
    assert retrieved_user is not None
    assert retrieved_user.id == test_user.id
    assert retrieved_user.name == test_user.name
    assert retrieved_user.email == test_user.email

# READ all users
def test_get_all_users(db_session):
    create_user(db=db_session, name="Bob Johnson", email="bob.johnson@example.com")
    create_user(db=db_session, name="Charlie Brown", email="charlie.brown@example.com")
    all_users = get_all_users(db=db_session)
    assert len(all_users) == 2

# UPDATE
def test_update_user_name(db_session, test_user):
    new_name = "Eve Black"
    updated_user = update_user_name(db=db_session, user_id=test_user.id, new_name=new_name)
    assert updated_user is not None
    assert updated_user.name == new_name
    assert updated_user.email == test_user.email

# DELETE
def test_delete_user(db_session, test_user):
    deleted_user = delete_user(db=db_session, user_id=test_user.id)
    assert deleted_user is not None
    assert deleted_user.id == test_user.id

    # Ensure the user is deleted
    retrieved_user = get_user_by_id(db=db_session, user_id=test_user.id)
    assert retrieved_user is None