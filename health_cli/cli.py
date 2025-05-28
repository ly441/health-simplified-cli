
import typer
from typing import Optional
from sqlalchemy.orm import Session
from health_cli.db.database import Base,engine
from health_cli.db.config import config
from health_cli.commands.goals import goals
from health_cli.commands.reporting import reporting
from health_cli.commands.meal_planning import meal_planning
from health_cli.commands.user_commands import user_commands
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

if __name__ == "__main__":
    app()