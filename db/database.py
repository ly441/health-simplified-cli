
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from db.config import config

# Get database configuration
driver = config.get('database', 'driver')
database_name = config.get('database', 'database_name')
host = config.get('database', 'host')
port = config.get('database', 'port')
username = config.get('database', 'username')
password = config.get('database', 'password')
echo_sql = config.getboolean('database', 'echo_sql')

if driver == 'sqlite':
    SQLALCHEMY_DATABASE_URL = f"sqlite:///{database_name}"
elif driver in ['postgresql', 'mysql']:
    SQLALCHEMY_DATABASE_URL = f"{driver}://{username}:{password}@{host}:{port}/{database_name}"
else:
    raise ValueError(f"Unsupported database driver: {driver}")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False} if driver == 'sqlite' else {},
    echo=echo_sql
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()