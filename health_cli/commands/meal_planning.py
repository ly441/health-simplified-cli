
import typer
from typing import Optional, List
from sqlalchemy.orm import Session
from health_cli.models import MealPlan, User
from db.database import get_db

app = typer.Typer(help="Manage your weekly meal plans")

# Constants
DAYS_OF_WEEK: List[str] = [
    "monday", "tuesday", "wednesday", 
    "thursday", "friday", "saturday", "sunday"
]

def get_user(db: Session, username: str) -> User:
    """Helper function to get user with error handling"""
    user = db.query(User).filter(User.name == username).first()
    if not user:
        typer.echo(f"Error: User '{username}' not found")
        raise typer.Exit(code=1)
    return user

def get_meal_plan(db: Session, user_id: int, week: int) -> Optional[MealPlan]:
    """Get existing meal plan or return None"""
    return db.query(MealPlan).filter(
        MealPlan.user_id == user_id,
        MealPlan.week_number == week
    ).first()

@app.command(name="create")
def plan_meal(
    user: str = typer.Argument(..., help="Username"),
    week: int = typer.Argument(..., help="Week number (1-52)", min=1, max=52)
):
    """
    Create or update a weekly meal plan interactively
    """
    db: Session = next(get_db())
    
    try:
        user_obj = get_user(db, user)
        plan = get_meal_plan(db, user_obj.id, week)
        
        if not plan:
            plan = MealPlan(user_id=user_obj.id, week_number=week)
            db.add(plan)
            db.commit()
            typer.echo(f"Created new meal plan for week {week}")
        else:
            typer.echo(f"Updating existing meal plan for week {week}")
        
        # Interactive editing with validation
        for day in DAYS_OF_WEEK:
            current_value = getattr(plan, day, "")
            new_value = typer.prompt(
                f"{day.capitalize()} meals",
                default=current_value if current_value else "Not specified",
                show_default=True
            )
            setattr(plan, day, new_value.strip())
        
        db.commit()
        typer.echo(typer.style(
            f"✅ Meal plan for week {week} saved successfully!",
            fg=typer.colors.GREEN
        ))
        
    except Exception as e:
        db.rollback()
        typer.echo(typer.style(
            f"❌ Error saving meal plan: {str(e)}",
            fg=typer.colors.RED
        ))
        raise typer.Exit(code=1)

@app.command(name="update")
def update_meal_day(
    plan_id: int = typer.Argument(..., help="Meal plan ID to update"),
    day: str = typer.Argument(
        ..., 
        help="Day of week to update",
        autocompletion=lambda: DAYS_OF_WEEK
    ),
    meal: str = typer.Argument(..., help="New meal description")
):
    """
    Update a specific day in a meal plan
    """
    db: Session = next(get_db())
    
    try:
        # Validate day input
        day = day.lower()
        if day not in DAYS_OF_WEEK:
            typer.echo(typer.style(
                f"Error: '{day}' is not a valid day. Use one of: {', '.join(DAYS_OF_WEEK)}",
                fg=typer.colors.RED
            ))
            raise typer.Exit(code=1)
        
        # Get and validate meal plan
        plan = db.query(MealPlan).get(plan_id)
        if not plan:
            typer.echo(typer.style(
                f"Error: Meal plan with ID {plan_id} not found",
                fg=typer.colors.RED
            ))
            raise typer.Exit(code=1)
        
        # Update the plan
        setattr(plan, day, meal.strip())
        db.commit()
        
        typer.echo(typer.style(
            f"✅ Updated {day.capitalize()} in week {plan.week_number}'s meal plan",
            fg=typer.colors.GREEN
        ))
        
    except Exception as e:
        db.rollback()
        typer.echo(typer.style(
            f"❌ Error updating meal plan: {str(e)}",
            fg=typer.colors.RED
        ))
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()