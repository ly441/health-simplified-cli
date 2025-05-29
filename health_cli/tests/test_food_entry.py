import pytest
from sqlalchemy.orm import Session
from datetime import date
from health_cli.db.database import Base, engine, SessionLocal
from health_cli.models.food_entry import FoodEntry
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

def test_food_entry_crud(db_session, test_user):
    # CREATE
    food_entry = FoodEntry(
        food="Apple",
        calories=95,
        date=date.today(),
        user_id=test_user.id
    )
    db_session.add(food_entry)
    db_session.commit()
    db_session.refresh(food_entry)

    assert food_entry.id is not None
    assert food_entry.food == "Apple"
    assert food_entry.calories == 95
    assert food_entry.date == date.today()
    assert food_entry.user_id == test_user.id

    # READ
    retrieved_entry = db_session.query(FoodEntry).filter(FoodEntry.id == food_entry.id).first()
    assert retrieved_entry is not None
    assert retrieved_entry.food == "Apple"
    assert retrieved_entry.calories == 95
    assert retrieved_entry.date == date.today()
    assert retrieved_entry.user_id == test_user.id

    # UPDATE
    retrieved_entry.food = "Grapes"
    retrieved_entry.calories = 70
    db_session.commit()
    db_session.refresh(retrieved_entry)

    assert retrieved_entry.food == "Grapes"
    assert retrieved_entry.calories == 70

    # DELETE
    db_session.delete(retrieved_entry)
    db_session.commit()

    deleted_entry = db_session.query(FoodEntry).filter(FoodEntry.id == food_entry.id).first()
    assert deleted_entry is None