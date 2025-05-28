
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float
from sqlalchemy.orm import relationship,Session
from db.database import Base

from models import MealPlan



class FoodEntry(Base):
    __tablename__ = 'food_entries'
    id = Column(Integer, primary_key=True)
    food = Column(String, nullable=False)
    calories = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="food_entries")



# CREATE
def create_meal_plan(db: Session, week_number: int, user_id: int, days: dict):
    meal_plan = MealPlan(
        week_number=week_number,
        user_id=user_id,
        monday=days.get("monday"),
        tuesday=days.get("tuesday"),
        wednesday=days.get("wednesday"),
        thursday=days.get("thursday"),
        friday=days.get("friday"),
        saturday=days.get("saturday"),
        sunday=days.get("sunday"),
    )
    db.add(meal_plan)
    db.commit()
    db.refresh(meal_plan)
    return meal_plan

# READ
def get_meal_plan_by_id(db: Session, meal_plan_id: int):
    return db.query(MealPlan).filter(MealPlan.id == meal_plan_id).first()

def get_all_meal_plans(db: Session):
    return db.query(MealPlan).all()

def get_meal_plans_by_user(db: Session, user_id: int):
    return db.query(MealPlan).filter(MealPlan.user_id == user_id).all()

# UPDATE
def update_meal_plan(db: Session, meal_plan_id: int, updated_data: dict):
    meal_plan = db.query(MealPlan).filter(MealPlan.id == meal_plan_id).first()
    if meal_plan:
        for day, value in updated_data.items():
            if hasattr(meal_plan, day):
                setattr(meal_plan, day, value)
        db.commit()
        db.refresh(meal_plan)
    return meal_plan

# DELETE
def delete_meal_plan(db: Session, meal_plan_id: int):
    meal_plan = db.query(MealPlan).filter(MealPlan.id == meal_plan_id).first()
    if meal_plan:
        db.delete(meal_plan)
        db.commit()
    return meal_plan

