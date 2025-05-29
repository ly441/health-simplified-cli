import pytest
from sqlalchemy.orm import Session
from datetime import date
from health_cli.db.database import Base, engine, SessionLocal
from health_cli.models.mealplan_entry import (
    create_meal_plan,
    get_meal_plan_by_id,
    get_all_meal_plans,
    get_meal_plans_by_user,
    update_meal_plan,
    delete_meal_plan,
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
        from health_cli.models.mealplan_entry import MealPlan
        from health_cli.models.users_entry import User

        session.query(MealPlan).delete()
        session.query(User).delete()
        session.commit()
        session.close()


# Fixture to create a test user
@pytest.fixture
def test_user(db_session):
    user = User(name="Test User", email="test@example.com")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

# CREATE
def test_create_meal_plan(db_session, test_user):
    days = {
        "monday": "Salad",
        "tuesday": "Pizza",
        "wednesday": "Burger",
        "thursday": "Sushi",
        "friday": "Steak",
        "saturday": "Pasta",
        "sunday": "Taco"
    }
    meal_plan = create_meal_plan(
        db=db_session,
        week_number=1,
        user_id=test_user.id,
        days=days
    )
    assert meal_plan.id is not None
    assert meal_plan.week_number == 1
    assert meal_plan.user_id == test_user.id
    assert meal_plan.monday == "Salad"
    assert meal_plan.tuesday == "Pizza"
    assert meal_plan.wednesday == "Burger"
    assert meal_plan.thursday == "Sushi"
    assert meal_plan.friday == "Steak"
    assert meal_plan.saturday == "Pasta"
    assert meal_plan.sunday == "Taco"

# READ by meal_plan_id
def test_get_meal_plan_by_id(db_session, test_user):
    days = {
        "monday": "Salad",
        "tuesday": "Pizza",
        "wednesday": "Burger",
        "thursday": "Sushi",
        "friday": "Steak",
        "saturday": "Pasta",
        "sunday": "Taco"
    }
    created_meal_plan = create_meal_plan(
        db=db_session,
        week_number=1,
        user_id=test_user.id,
        days=days
    )
    retrieved_meal_plan = get_meal_plan_by_id(db=db_session, meal_plan_id=created_meal_plan.id)
    assert retrieved_meal_plan is not None
    assert retrieved_meal_plan.id == created_meal_plan.id
    assert retrieved_meal_plan.week_number == 1
    assert retrieved_meal_plan.user_id == test_user.id
    assert retrieved_meal_plan.monday == "Salad"
    assert retrieved_meal_plan.tuesday == "Pizza"
    assert retrieved_meal_plan.wednesday == "Burger"
    assert retrieved_meal_plan.thursday == "Sushi"
    assert retrieved_meal_plan.friday == "Steak"
    assert retrieved_meal_plan.saturday == "Pasta"
    assert retrieved_meal_plan.sunday == "Taco"

# READ all meal plans
def test_get_all_meal_plans(db_session, test_user):
    days1 = {
        "monday": "Salad",
        "tuesday": "Pizza",
        "wednesday": "Burger",
        "thursday": "Sushi",
        "friday": "Steak",
        "saturday": "Pasta",
        "sunday": "Taco"
    }
    days2 = {
        "monday": "Soup",
        "tuesday": "Sandwich",
        "wednesday": "Taco",
        "thursday": "Salad",
        "friday": "Pizza",
        "saturday": "Burger",
        "sunday": "Sushi"
    }
    create_meal_plan(db=db_session, week_number=1, user_id=test_user.id, days=days1)
    create_meal_plan(db=db_session, week_number=2, user_id=test_user.id, days=days2)
    all_meal_plans = get_all_meal_plans(db=db_session)
    assert len(all_meal_plans) == 2

# READ meal plans by user_id
def test_get_meal_plans_by_user(db_session, test_user):
    days = {
        "monday": "Salad",
        "tuesday": "Pizza",
        "wednesday": "Burger",
        "thursday": "Sushi",
        "friday": "Steak",
        "saturday": "Pasta",
        "sunday": "Taco"
    }
    create_meal_plan(db=db_session, week_number=1, user_id=test_user.id, days=days)
    user_meal_plans = get_meal_plans_by_user(db=db_session, user_id=test_user.id)
    assert len(user_meal_plans) == 1
    assert user_meal_plans[0].user_id == test_user.id

# UPDATE
def test_update_meal_plan(db_session, test_user):
    days = {
        "monday": "Salad",
        "tuesday": "Pizza",
        "wednesday": "Burger",
        "thursday": "Sushi",
        "friday": "Steak",
        "saturday": "Pasta",
        "sunday": "Taco"
    }
    created_meal_plan = create_meal_plan(
        db=db_session,
        week_number=1,
        user_id=test_user.id,
        days=days
    )
    updated_data = {
        "monday": "Soup",
        "tuesday": "Sandwich",
        "wednesday": "Taco",
        "thursday": "Salad",
        "friday": "Pizza",
        "saturday": "Burger",
        "sunday": "Sushi"
    }
    updated_meal_plan = update_meal_plan(db=db_session, meal_plan_id=created_meal_plan.id, updated_data=updated_data)
    assert updated_meal_plan is not None
    assert updated_meal_plan.monday == "Soup"
    assert updated_meal_plan.tuesday == "Sandwich"
    assert updated_meal_plan.wednesday == "Taco"
    assert updated_meal_plan.thursday == "Salad"
    assert updated_meal_plan.friday == "Pizza"
    assert updated_meal_plan.saturday == "Burger"
    assert updated_meal_plan.sunday == "Sushi"

# DELETE
def test_delete_meal_plan(db_session, test_user):
    days = {
        "monday": "Salad",
        "tuesday": "Pizza",
        "wednesday": "Burger",
        "thursday": "Sushi",
        "friday": "Steak",
        "saturday": "Pasta",
        "sunday": "Taco"
    }
    created_meal_plan = create_meal_plan(
        db=db_session,
        week_number=1,
        user_id=test_user.id,
        days=days
    )
    deleted_meal_plan = delete_meal_plan(db=db_session, meal_plan_id=created_meal_plan.id)
    assert deleted_meal_plan is not None
    assert deleted_meal_plan.id == created_meal_plan.id

    # Ensure the meal plan is deleted
    retrieved_meal_plan = get_meal_plan_by_id(db=db_session, meal_plan_id=created_meal_plan.id)
    assert retrieved_meal_plan is None