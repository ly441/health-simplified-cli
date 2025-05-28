import typer
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models import FoodEntry, Goal, User
from ...db.database import get_db

app = typer.Typer()

@app.command()
def report(user: str, report_date: date):
    """Generate a nutrition report for a user on a specific date"""
    db: Session = next(get_db())
    
    user_obj = db.query(User).filter(User.name == user).first()
    if not user_obj:
        typer.echo(f"User {user} not found")
        raise typer.Exit(code=1)
    
    # Get total calories for the day
    total_calories = db.query(func.sum(FoodEntry.calories)).filter(
        FoodEntry.user_id == user_obj.id,
        FoodEntry.date == report_date
    ).scalar() or 0
    
    # Get user's daily goal
    goal = db.query(Goal).filter(Goal.user_id == user_obj.id).first()
    daily_goal = goal.daily_calories if goal else None
    
    # Generate report
    typer.echo(f"Nutrition Report for {user} on {report_date}:")
    typer.echo(f"Total Calories Consumed: {total_calories}")
    
    if daily_goal:
        remaining = daily_goal - total_calories
        typer.echo(f"Daily Goal: {daily_goal}")
        typer.echo(f"Remaining: {remaining} ({remaining/daily_goal:.1%} of goal left)")
        if total_calories > daily_goal:
            typer.echo(typer.style("You've exceeded your daily goal!", fg=typer.colors.RED))
        else:
            typer.echo(typer.style("You're on track!", fg=typer.colors.GREEN))
    else:
        typer.echo("No daily goal set. Use 'goal set' to set targets.")
