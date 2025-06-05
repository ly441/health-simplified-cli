
import typer
from sqlalchemy.orm import Session
from datetime import date
from health_cli.db.database import SessionLocal
from health_cli.models.users_entry import User
from health_cli.models.goals_entry import Goal
from health_cli.models.mealplan_entry import MealPlan
from health_cli.models.food_entry import FoodEntry

app = typer.Typer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.command()
def cli():
    while True:
        choice = main_menu()
        if choice == 1:
            add_user()
        elif choice == 2:
            update_user()
        elif choice == 3:
            delete_user()
        elif choice == 4:
            add_goal()
        elif choice == 5:
            update_goal()
        elif choice == 6:
            delete_goal()
        elif choice == 7:
            add_mealplan()
        elif choice == 8:
            update_mealplan()
        elif choice == 9:
            delete_mealplan()
        elif choice == 10:
            list_user_details()
        elif choice ==11:
            add_food_entry()
        elif choice ==12:
            update_food_entry()
        elif choice ==13:
          delete_food_entry()            
        elif choice == 0:
            typer.echo("Exiting...")
            break
        else:
            typer.echo("Invalid choice. Please try again.")

def main_menu():
    typer.echo("Welcome to Health Simplified CLI")
    typer.echo("1. Add User")
    typer.echo("2. Update User")
    typer.echo("3. Delete User")
    typer.echo("4. Add Goal")
    typer.echo("5. Update Goal")
    typer.echo("6. Delete Goal")
    typer.echo("7. Add Meal Plan")
    typer.echo("8. Update Meal Plan")
    typer.echo("9. Delete Meal Plan")
    typer.echo("10. List User Details")
    typer.echo("11.Add Food Entry")
    typer.echo("12.Update Food Entry")
    typer.echo("13.Delete Food Entry")
    typer.echo("0. Exit")
    choice = typer.prompt("Please select an option", type=int)
    return choice


def add_food_entry():
    """Add a new food entry for a user"""
    user_id = typer.prompt("Enter user ID", type=int)
    food = typer.prompt("Enter food item")
    calories = typer.prompt("Enter calories", type=int)
    entry_date = typer.prompt("Enter date (YYYY-MM-DD)")

    try:
        parsed_date = date.fromisoformat(entry_date)
    except ValueError:
        typer.echo("❌ Invalid date format. Use YYYY-MM-DD.")
        return

    db = SessionLocal()
    try:
        food_entry = FoodEntry(user_id=user_id, food=food, calories=calories, date=parsed_date)
        db.add(food_entry)
        db.commit()
        db.refresh(food_entry)
        typer.echo(f"✅ Food entry added for user {user_id}: {food} ({calories} calories) on {parsed_date}")
    except Exception as e:
        db.rollback()
        typer.echo(f"❌ Failed to add food entry: {e}")
    finally:
        db.close()

def create_food_entry():
    """Add a new food entry for a user"""
    user_id = typer.prompt("Enter user ID", type=int)
    food = typer.prompt("Enter food item")
    calories = typer.prompt("Enter calories", type=int)
    entry_date = typer.prompt("Enter date (YYYY-MM-DD)")

    try:
        parsed_date = date.fromisoformat(entry_date)
    except ValueError:
        typer.echo("❌ Invalid date format. Use YYYY-MM-DD.")
        return

    db = SessionLocal()
    try:
        food_entry = create_food_entry(db, user_id, food, calories, parsed_date)
        typer.echo(f"✅ Food entry added for user {user_id}: {food} ({calories} calories) on {parsed_date}")
    except Exception as e:
        db.rollback()
        typer.echo(f"❌ Failed to add food entry: {e}")
    finally:
        db.close()

def update_food_entry_cli():
    """Update an existing food entry"""
    entry_id = typer.prompt("Enter food entry ID", type=int)
    food = typer.prompt("Enter new food item (leave blank to keep current)", default="")
    calories = typer.prompt("Enter new calories (leave blank to keep current)", default="")
    entry_date = typer.prompt("Enter new date (YYYY-MM-DD) (leave blank to keep current)", default="")

    db = SessionLocal()
    try:
        if calories:
            calories = int(calories)
        if entry_date:
            entry_date = date.fromisoformat(entry_date)
        food_entry = update_food_entry(db, entry_id, food, calories, entry_date)
        typer.echo(f"✅ Food entry with ID {entry_id} updated.")
    except Exception as e:
        db.rollback()
        typer.echo(f"❌ Failed to update food entry: {e}")
    finally:
        db.close()

def delete_food_entry():
    """Delete a food entry"""
    entry_id = typer.prompt("Enter food entry ID", type=int)

    db = SessionLocal()
    try:
        food_entry = delete_food_entry(db, entry_id)
        typer.echo(f"✅ Food entry with ID {entry_id} deleted.")
    except Exception as e:
        db.rollback()
        typer.echo(f"❌ Failed to delete food entry: {e}")
    finally:
        db.close()

def add_user():
    """Add a new user with prompts"""
    name = typer.prompt("Enter user's name")
    email = typer.prompt("Enter user's email")
    
    db = SessionLocal()
    try:
        user = User(name=name, email=email)
        db.add(user)
        db.commit()
        db.refresh(user)
        typer.echo(f"✅ User '{name}' added with ID {user.id}")
    except Exception as e:
        db.rollback()
        typer.echo(f"❌ Failed to add user: {e}")
    finally:
        db.close()

def update_user():
    """Update an existing user"""
    user_id = typer.prompt("Enter user ID", type=int)
    name = typer.prompt("Enter new name (leave blank to keep current)", default="")
    email = typer.prompt("Enter new email (leave blank to keep current)", default="")

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            typer.echo("❌ User not found.")
            return

        if name:
            user.name = name
        if email:
            user.email = email

        db.commit()
        typer.echo(f"✅ User with ID {user_id} updated.")
    except Exception as e:
        db.rollback()
        typer.echo(f"❌ Failed to update user: {e}")
    finally:
        db.close()

def delete_user():
    """Delete a user"""
    user_id = typer.prompt("Enter user ID", type=int)

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            typer.echo("❌ User not found.")
            return

        db.delete(user)
        db.commit()
        typer.echo(f"✅ User with ID {user_id} deleted.")
    except Exception as e:
        db.rollback()
        typer.echo(f"❌ Failed to delete user: {e}")
    finally:
        db.close()

def add_goal():
    """Add a new goal for a user"""
    user_id = typer.prompt("Enter user ID", type=int)
    description = typer.prompt("Enter goal description")
    
    while True:
        target = typer.prompt("Enter goal target (numeric value only)")
        try:
            target = float(target)
            break
        except ValueError:
            typer.echo("Error: Please enter a valid numeric value for the goal target.")

    goal_date = typer.prompt("Enter goal date (YYYY-MM-DD)")
    
    try:
        parsed_date = date.fromisoformat(goal_date)
    except ValueError:
        typer.echo("❌ Invalid date format. Use YYYY-MM-DD.")
        return

    db = SessionLocal()
    try:
        goal = Goal(user_id=user_id, description=description, target=target, date=parsed_date)
        db.add(goal)
        db.commit()
        db.refresh(goal)
        typer.echo(f"🎯 Goal for user {user_id} added on {parsed_date}: {description}")
    except Exception as e:
        db.rollback()
        typer.echo(f"❌ Failed to add goal: {e}")
    finally:
        db.close()

def update_goal():
    """Update an existing goal"""
    goal_id = typer.prompt("Enter goal ID", type=int)
    description = typer.prompt("Enter new description (leave blank to keep current)", default="")
    target = typer.prompt("Enter new target (leave blank to keep current)", default="")
    goal_date = typer.prompt("Enter new date (YYYY-MM-DD) (leave blank to keep current)", default="")

    db = SessionLocal()
    try:
        goal = db.query(Goal).filter(Goal.id == goal_id).first()
        if not goal:
            typer.echo("❌ Goal not found.")
            return

        if description:
            goal.description = description
        if target:
            goal.target = float(target)
        if goal_date:
            goal.date = date.fromisoformat(goal_date)

        db.commit()
        typer.echo(f"✅ Goal with ID {goal_id} updated.")
    except Exception as e:
        db.rollback()
        typer.echo(f"❌ Failed to update goal: {e}")
    finally:
        db.close()

def add_mealplan():
    """Add a weekly meal plan"""
    user_id = typer.prompt("Enter user ID", type=int)
    week = typer.prompt("Enter week number", type=int)
    meals = {}
    for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
        meals[day] = typer.prompt(f"Meal for {day.capitalize()}")

    db = SessionLocal()
    try:
        plan = MealPlan(
            user_id=user_id,
            week_number=week,
            **meals
        )
        db.add(plan)
        db.commit()
        db.refresh(plan)
        typer.echo(f"🍽️ Meal plan for user {user_id}, week {week} added.")
    except Exception as e:
        db.rollback()
        typer.echo(f"❌ Failed to add meal plan: {e}")
    finally:
        db.close()

def update_mealplan():
    """Update an existing meal plan"""
    plan_id = typer.prompt("Enter meal plan ID", type=int)
    week = typer.prompt("Enter new week number (leave blank to keep current)", default="")
    meals = {}
    for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
        meals[day] = typer.prompt(f"Meal for {day.capitalize()} (leave blank to keep current)", default="")

    db = SessionLocal()
    try:
        plan = db.query(MealPlan).filter(MealPlan.id == plan_id).first()
        if not plan:
            typer.echo("❌ Meal plan not found.")
            return

        if week:
            plan.week_number = int(week)
        for day, meal in meals.items():
            if meal:
                setattr(plan, day, meal)

        db.commit()
        typer.echo(f"✅ Meal plan with ID {plan_id} updated.")
    except Exception as e:
        db.rollback()
        typer.echo(f"❌ Failed to update meal plan: {e}")
    finally:
        db.close()

def delete_mealplan():
    """Delete a meal plan"""
    plan_id = typer.prompt("Enter meal plan ID", type=int)

    db = SessionLocal()
    try:
        plan = db.query(MealPlan).filter(MealPlan.id == plan_id).first()
        if not plan:
            typer.echo("❌ Meal plan not found.")
            return

        db.delete(plan)
        db.commit()
        typer.echo(f"✅ Meal plan with ID {plan_id} deleted.")
    except Exception as e:
        db.rollback()
        typer.echo(f"❌ Failed to delete meal plan: {e}")
    finally:
        db.close()





def list_user_details():
    """List all details of a specific user"""
    user_id = typer.prompt("Enter user ID", type=int)

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            typer.echo("❌ User not found.")
            return

        typer.echo(f"User Details:")
        typer.echo(f"ID: {user.id}")
        typer.echo(f"Name: {user.name}")
        typer.echo(f"Email: {user.email}")

        typer.echo("\nGoals:")
        if user.goals:
            goal = user.goals
            for goal in user.goals:
                typer.echo(f"  ID: {goal.id}, Description: {goal.description}, Target: {goal.target}, Date: {goal.date}")
        else:
            typer.echo("  No goals found.")

        typer.echo("\nMeal Plans:")
        if user.meal_plans:
            for mealplan in user.meal_plans:
                typer.echo(f"  Week: {mealplan.week_number}")
                for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
                    typer.echo(f"    {day.capitalize()}: {getattr(mealplan, day)}")
        else:
            typer.echo("  No meal plans found.")

        typer.echo("\nFood Entries:")
        if user.food_entries:
            for entry in user.food_entries:
                typer.echo(f"  ID: {entry.id}, Food: {entry.food}, Calories: {entry.calories}, Date: {entry.date}")
        else:
            typer.echo("  No food entries found.")

    except Exception as e:
        typer.echo(f"❌ Failed to list user details: {e}")
    finally:
        db.close()
if __name__ == "__main__":
    app()