import typer
from .commands import goals, reporting, meal_planning

app = typer.Typer()
app.add_typer(goals.app, name="goal")
app.add_typer(reporting.app, name="report")
app.add_typer(meal_planning.app, name="plan-meal")

if __name__ == "__main__":
    app()