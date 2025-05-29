
import pytest
from sqlalchemy.orm import Session
from datetime import date
from health_cli.db.database import Base, engine, SessionLocal
from health_cli.models.goals_entry import Goal
from health_cli.models.users_entry import User
from health_cli.models.goals_entry import (
    create_goal,
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
        session.query(Goal).delete()
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
def test_create_goal(db_session, test_user):
    goal = create_goal(
        db=db_session,
        user_id=test_user.id,
        daily_calories=2000,
        weekly_calories=14000,
        description="Lose 10 pounds",
        target=10.0,
        date=date.today()
    )
    assert goal.id is not None
    assert goal.daily_calories == 2000
    assert goal.weekly_calories == 14000
    assert goal.description == "Lose 10 pounds"
    assert goal.target == 10.0
    assert goal.date == date.today()
    assert goal.user_id == test_user.id