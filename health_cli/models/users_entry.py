from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float
from sqlalchemy.orm import relationship
from db.database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    food_entries = relationship("FoodEntry", back_populates="user")
    goals = relationship("Goal", back_populates="user", uselist=False)
    meal_plans = relationship("MealPlan", back_populates="user")

class FoodEntry(Base):
    __tablename__ = 'food_entries'
    id = Column(Integer, primary_key=True)
    food = Column(String, nullable=False)
    calories = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="food_entries")

class Goal(Base):
    __tablename__ = 'goals'
    id = Column(Integer, primary_key=True)
    daily_calories = Column(Integer)
    weekly_calories = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)
    user = relationship("User", back_populates="goals")

class MealPlan(Base):
    __tablename__ = 'meal_plans'
    id = Column(Integer, primary_key=True)
    week_number = Column(Integer, nullable=False)
    monday = Column(String)
    tuesday = Column(String)
    wednesday = Column(String)
    thursday = Column(String)
    friday = Column(String)
    saturday = Column(String)
    sunday = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="meal_plans")

