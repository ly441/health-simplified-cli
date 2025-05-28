
import typer
from typing import Optional
from health_cli.db.database import Base
from health_cli.db.config import config
from health_cli.commands import goals, reporting, meal_planning,user_commands

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
app.add_typer(user_commands.app,name="user")

if __name__ == "__main__":
    app()