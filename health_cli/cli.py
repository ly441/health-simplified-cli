
import typer
from typing import Optional
from sqlalchemy.orm import Session
from health_cli.db.database import Base,engine
from health_cli.db.config import config
from health_cli.commands.goals import Goal
from datetime import date
from health_cli.commands.reporting import reporting
from health_cli.commands.meal_planning import MealPlan
from health_cli.commands.user_commands import User
from health_cli.models.users_entry import User


Base.metadata.create_all(bind=engine)

app = typer.Typer()

# Set default user from config if available
default_user = config.get('cli', 'default_user')

@app.callback()
def create_user(name: str, email: str):
    db = Session(engine)
    try:
        user = User(name=name, email=email)
        db.add(user)
        db.commit()
        typer.echo(f"Created user: {name}")
    finally:
        db.close()

 
 


# 🔹 Add user (with prompts)
@app.command()
def add_user():
    """Add a new user with prompts"""
    name = typer.prompt("Enter user's name")
    email = typer.prompt("Enter user's email")
    db = Session()
    user = User(name=name, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    typer.echo(f"✅ User '{name}' added with ID {user.id}")

# 🔹 Add goal (with prompts and date)
@app.command()
def add_goal():
    """Add a new goal for a user"""
    user_id = typer.prompt("Enter user ID", type=int)
    description = typer.prompt("Enter goal description")
    target = typer.prompt("Enter goal target", type=float)
    goal_date = typer.prompt("Enter goal date (YYYY-MM-DD)")
    
    try:
        parsed_date = date.fromisoformat(goal_date)
    except ValueError:
        typer.echo("❌ Invalid date format. Use YYYY-MM-DD.")
        raise typer.Exit()

    db = Session()
    goal = Goal(user_id=user_id, description=description, target=target, date=parsed_date)
    db.add(goal)
    db.commit()
    db.refresh(goal)
    db.close()
    typer.echo(f"🎯 Goal for user {user_id} added on {parsed_date}: {description}")

# 🔹 Add meal plan (with prompts)
@app.command()
def add_mealplan():
    """Add a weekly meal plan"""
    user_id = typer.prompt("Enter user ID", type=int)
    week = typer.prompt("Enter week number", type=int)
    meals = {}
    for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
        meals[day] = typer.prompt(f"Meal for {day.capitalize()}")

    db = Session()
    plan = MealPlan(
        user_id=user_id,
        week_number=week,
        **meals
    )
    db.add(plan)
    db.commit()
    db.refresh(plan)
    db.close()
    typer.echo(f"🍽️ Meal plan for user {user_id}, week {week} added.")




if __name__ == "__main__":
    app()