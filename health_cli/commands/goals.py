import typer
from typing import Optional
from datetime import date
from sqlalchemy.orm import Session
from ..models import Goal, User
from ...db.database import get_db

app = typer.Typer()

@app.command()
def set(user: str, daily: int, weekly: int):
    """Set daily and weekly calorie goals for a user"""
    db: Session = next(get_db())
    
    user_obj = db.query(User).filter(User.name == user).first()
    if not user_obj:
        typer.echo(f"User {user} not found")
        raise typer.Exit(code=1)
    
    goal = db.query(Goal).filter(Goal.user_id == user_obj.id).first()
    if not goal:
        goal = Goal(user_id=user_obj.id)
        db.add(goal)
    
    goal.daily_calories = daily
    goal.weekly_calories = weekly
    db.commit()
    
    typer.echo(f"Goals set for {user}: Daily={daily}, Weekly={weekly}")

@app.command()
def list(user: str):
    """List goals for a user"""
    db: Session = next(get_db())
    
    user_obj = db.query(User).filter(User.name == user).first()
    if not user_obj:
        typer.echo(f"User {user} not found")
        raise typer.Exit(code=1)
    
    goal = db.query(Goal).filter(Goal.user_id == user_obj.id).first()
    if goal:
        typer.echo(f"Goals for {user}:")
        typer.echo(f"  Daily: {goal.daily_calories} calories")
        typer.echo(f"  Weekly: {goal.weekly_calories} calories")
    else:
        typer.echo(f"No goals set for {user}")