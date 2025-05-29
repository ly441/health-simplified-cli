
import pytest
from sqlalchemy.orm import Session
from datetime import date
from health_cli.db.database import Base, engine, SessionLocal
from health_cli.models.food_entry import FoodEntry
from health_cli.models.users_entry import User

# Create all tables
Base.metadata.create_all(bind=engine)

# Fixture to create a database session
@pytest.fixture(autouse=True)
def db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.query(FoodEntry).delete()
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
def test_create_food_entry(db_session, test_user):
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