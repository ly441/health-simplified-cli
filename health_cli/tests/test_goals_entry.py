import pytest
from sqlalchemy.orm import Session
from datetime import date
from health_cli.db.database import Base, engine, SessionLocal
from health_cli.models.goals_entry import (
    create_goal,
    get_goal_by_user_id,
    get_goal_by_id,
    update_goal,
    delete_goal,
)
from health_cli.models.users_entry import User

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

# Fixture to create a test user
@pytest.fixture
def test_user(db_session):
    user = User(name="Test User", email="test@example.com")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

def test_goal_crud(db_session, test_user):
    # CREATE
    goal = create_goal(
        db=db_session,
        user_id=test_user.id,
        daily_calories=2000,
        weekly_calories=14000
    )
    assert goal.id is not None
    assert goal.daily_calories == 2000
    assert goal.weekly_calories == 14000
    assert goal.user_id == test_user.id

    # READ by user_id
    retrieved_goal_by_user = get_goal_by_user_id(db=db_session, user_id=test_user.id)
    assert retrieved_goal_by_user is not None
    assert retrieved_goal_by_user.id == goal.id
    assert retrieved_goal_by_user.daily_calories == 2000
    assert retrieved_goal_by_user.weekly_calories == 14000
    assert retrieved_goal_by_user.user_id == test_user.id

    # READ by goal_id
    retrieved_goal_by_id = get_goal_by_id(db=db_session, goal_id=goal.id)
    assert retrieved_goal_by_id is not None
    assert retrieved_goal_by_id.id == goal.id
    assert retrieved_goal_by_id.daily_calories == 2000
    assert retrieved_goal_by_id.weekly_calories == 14000
    assert retrieved_goal_by_id.user_id == test_user.id

    # UPDATE
    updated_data = {
        "daily_calories": 2200,
        "weekly_calories": 15400
    }
    updated_goal = update_goal(db=db_session, goal_id=goal.id, updated_data=updated_data)
    assert updated_goal is not None
    assert updated_goal.daily_calories == 2200
    assert updated_goal.weekly_calories == 15400

    # DELETE
    deleted_goal = delete_goal(db=db_session, goal_id=goal.id)
    assert deleted_goal is not None
    assert deleted_goal.id == goal.id

    # Ensure the goal is deleted
    retrieved_goal = get_goal_by_id(db=db_session, goal_id=goal.id)
    assert retrieved_goal is None