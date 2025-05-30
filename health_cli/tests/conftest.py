import pytest
from sqlalchemy.orm import Session
from health_cli.db.database import Base, engine, SessionLocal
from health_cli.models.food_entry import FoodEntry
from health_cli.models.users_entry import User
from health_cli.models.goals_entry import Goal
from health_cli.models.mealplan_entry import MealPlan

# Fixture to create a database session
@pytest.fixture(autouse=True)
def db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.query(User).delete()
        session.query(Goal).delete()
        session.query(FoodEntry).delete()
        session.query(MealPlan).delete()
        session.commit()
        session.close()

# Fixture to create all tables once
@pytest.fixture(scope="session", autouse=True)
def create_tables():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    