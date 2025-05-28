
import typer
from typing import Optional
from db.config import config
from .commands import goals, reporting, meal_planning

app = typer.Typer()

# Set default user from config if available
default_user = config.get('cli', 'default_user')

@app.callback()
def main(ctx: typer.Context, user: Optional[str] = default_user):
    """Health Simplified CLI - Track your nutrition from the command line"""
    if user:
        ctx.obj = {'user': user}

app.add_typer(goals.app, name="goal")
app.add_typer(reporting.app, name="report")
app.add_typer(meal_planning.app, name="plan-meal")

if __name__ == "__main__":
    app()