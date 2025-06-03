
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./health.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    from health_cli.models.users_entry import User
    from health_cli.models.food_entry import FoodEntry
    from health_cli.models.goals_entry import Goal
    from health_cli.models.mealplan_entry import MealPlan
    print("Creating tables if they don't exist...")
    Base.metadata.create_all(bind=engine)
