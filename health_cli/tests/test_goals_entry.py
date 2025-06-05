
import pytest
from sqlalchemy.orm import Session
from datetime import date
from health_cli.db.database import Base, engine, SessionLocal
from health_cli.models.goals_entry import Goal, create_goal
from health_cli.models.users_entry import User

# Automatically create tables for test session
@pytest.fixture(scope="session", autouse=True)
def create_tables():
    Base.metadata.drop_all(bind=engine)  
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# Database session per test
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

# Fixture to create a unique test user
@pytest.fixture
def test_user(db_session, request):
    unique_id = request.node.name.replace("[", "_").replace("]", "_")  # Pytest param-safe
    user = User(name=f"Test User {unique_id}", email=f"user_{unique_id}@example.com")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

# Test: create goal
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
