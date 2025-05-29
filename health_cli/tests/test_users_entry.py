
import pytest
from sqlalchemy.orm import Session
from health_cli.db.database import Base, engine, SessionLocal
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
@pytest.fixture
def db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

# CREATE
def test_create_user(db_session):
    user = create_user(db=db_session, name="John Doe", email="john.doe@example.com")
    assert user.id is not None
    assert user.name == "John Doe"
    assert user.email == "john.doe@example.com"

# READ by user_id
def test_get_user_by_id(db_session):
    created_user = create_user(db=db_session, name="Jane Doe", email="jane.doe@example.com")
    retrieved_user = get_user_by_id(db=db_session, user_id=created_user.id)
    assert retrieved_user is not None
    assert retrieved_user.id == created_user.id
    assert retrieved_user.name == "Jane Doe"
    assert retrieved_user.email == "jane.doe@example.com"

# READ by name
def test_get_user_by_name(db_session):
    created_user = create_user(db=db_session, name="Alice Smith", email="alice.smith@example.com")
    retrieved_user = get_user_by_name(db=db_session, name="Alice Smith")
    assert retrieved_user is not None
    assert retrieved_user.id == created_user.id
    assert retrieved_user.name == "Alice Smith"
    assert retrieved_user.email == "alice.smith@example.com"

# READ all users
def test_get_all_users(db_session):
    create_user(db=db_session, name="Bob Johnson", email="bob.johnson@example.com")
    create_user(db=db_session, name="Charlie Brown", email="charlie.brown@example.com")
    all_users = get_all_users(db=db_session)
    assert len(all_users) == 2

# UPDATE
def test_update_user_name(db_session):
    created_user = create_user(db=db_session, name="Eve Davis", email="eve.davis@example.com")
    updated_user = update_user_name(db=db_session, user_id=created_user.id, new_name="Eve Black")
    assert updated_user is not None
    assert updated_user.name == "Eve Black"
    assert updated_user.email == "eve.davis@example.com"

# DELETE
def test_delete_user(db_session):
    created_user = create_user(db=db_session, name="Frank White", email="frank.white@example.com")
    deleted_user = delete_user(db=db_session, user_id=created_user.id)
    assert deleted_user is not None
    assert deleted_user.id == created_user.id

    # Ensure the user is deleted
    retrieved_user = get_user_by_id(db=db_session, user_id=created_user.id)
    assert retrieved_user is None