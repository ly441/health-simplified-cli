import typer
from typing import Optional
from sqlalchemy.orm import Session
from ..models import MealPlan, User
from ...db.database import get_db

app = typer.Typer()

@app.command()
def plan_meal(user: str, week: int):
    """Create or update a weekly meal plan"""
    db: Session = next(get_db())
    
    user_obj = db.query(User).filter(User.name == user).first()
    if not user_obj:
        typer.echo(f"User {user} not found")
        raise typer.Exit(code=1)
    
    # Check if plan exists for this week
    plan = db.query(MealPlan).filter(
        MealPlan.user_id == user_obj.id,
        MealPlan.week_number == week
    ).first()
    
    if not plan:
        plan = MealPlan(user_id=user_obj.id, week_number=week)
        db.add(plan)
        db.commit()
        typer.echo(f"Created new meal plan for week {week}")
    else:
        typer.echo(f"Updating existing meal plan for week {week}")
    
    # Interactive editing
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    for day in days:
        current = getattr(plan, day)
        new_value = typer.prompt(
            f"{day.capitalize()} meal plan",
            default=current if current else "",
            show_default=True
        )
        setattr(plan, day, new_value)
    
    db.commit()
    typer.echo("Meal plan saved successfully!")

@app.command()
def update(id: int, day: Optional[str] = None, meal: Optional[str] = None):
    """Update a specific day in a meal plan"""
    db: Session = next(get_db())
    
    plan = db.query(MealPlan).filter(MealPlan.id == id).first()
    if not plan:
        typer.echo(f"Meal plan with ID {id} not found")
        raise typer.Exit(code=1)
    
    if day and meal:
        if not hasattr(plan, day):
            typer.echo(f"Invalid day: {day}")
            raise typer.Exit(code=1)
        setattr(plan, day, meal)
        db.commit()
        typer.echo(f"Updated {day} in week {plan.week_number}'s meal plan")
    else:
        typer.echo("Please provide both --day and --meal parameters")
        raise typer.Exit(code=1)    