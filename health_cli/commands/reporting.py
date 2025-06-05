import typer
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
from health_cli.models.food_entry import FoodEntry
from health_cli.models.goals_entry import Goal
from health_cli.models.users_entry import User
from health_cli.db.database import get_db

app = typer.Typer()




@app.command()

def report(user: str, report_date: str):
    """Generate a nutrition report for a user on a specific date"""
    db: Session = next(get_db())

    try:
        report_date_parsed = datetime.strptime(report_date, "%Y-%m-%d").date()
    except ValueError:
        typer.echo("❌ Date must be in format YYYY-MM-DD")
        raise typer.Exit(code=1)

    user_obj = db.query(User).filter(User.name == user).first()
    if not user_obj:
        typer.echo(f"User {user} not found")
        raise typer.Exit(code=1)

    total_calories = db.query(func.sum(FoodEntry.calories)).filter(
        FoodEntry.user_id == user_obj.id,
        FoodEntry.date == report_date_parsed
    ).scalar() or 0
    
    # Get user's daily goal
    goal = db.query(Goal).filter(Goal.user_id == user_obj.id).first()
    daily_goal = goal.daily_calories if goal else None
    
    # Generate report
    typer.echo(f"Nutrition Report for {user} on {parsed_date}:")
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
