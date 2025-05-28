from health_cli.db.database import engine, Base
from health_cli.models.users_entry import User
from health_cli.models.goals_entry import Goal
from health_cli.models.mealplan_entry  import MealPlan
from health_cli.models.food_entry import FoodEntry


def init():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized.")

if __name__ == "__main__":
    init()
