from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float
from health_cli.db.database import Base
from sqlalchemy.orm import relationship, Session
from sqlalchemy.exc import  IntegrityError


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    food_entries = relationship("FoodEntry", back_populates="user",)
    goals = relationship("Goal", back_populates="user")
    meal_plans = relationship("MealPlan", back_populates="user")




# CREATE
def create_user(db: Session, name: str, email: str):
    try:
        user = User(name=name, email=email)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError:
        db.rollback()
        raise ValueError("User with this name or email already exists")

# READ
def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_name(db: Session, name: str):
    return db.query(User).filter(User.name == name).first()

def get_all_users(db: Session):
    return db.query(User).all()

# UPDATE
def update_user_name(db: Session, user_id: int, new_name: str):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        try:
            user.name = new_name
            db.commit()
            db.refresh(user)
        except IntegrityError:
            db.rollback()
            raise ValueError("User with this name already exists")
    return user

# DELETE
def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user