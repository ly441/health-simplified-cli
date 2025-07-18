import typer
from sqlalchemy.exc import IntegrityError
from health_cli.db.database import SessionLocal
from health_cli.models.users_entry import User

app = typer.Typer()

@app.command()
def create(name: str = typer.Option(..., prompt=True),
           email: str = typer.Option(..., prompt=True)):
    """Create new user"""
    with SessionLocal() as session:
        try:
            user = User(name=name, email=email)
            session.add(user)
            session.commit()
            typer.echo(f"Created user: {user}")
        except IntegrityError:
            session.rollback()
            typer.echo("Error: Email already exists!", err=True)

@app.command()
def list():
    """List all users"""
    with SessionLocal() as session:
        users = session.query(User).all()
        if not users:
            typer.echo("No users found")
            return
        
        for user in users:
            typer.echo(f"{user.id}: {user.name} ({user.email})")

@app.command()
def debug_users():
    db = SessionLocal()
    try:
        users = db.query(User).all()
        for user in users:
            print(user.id, user.name, user.email)
    finally:
        db.close()

           

