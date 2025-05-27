from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from .base import Base

class FoodEntry(Base):
    __tablename__ = "food_entries"

    id = Column(Integer, primary_key=True, index=True)
    food_name = Column(String(100), nullable=False)
    calories = Column(Integer, nullable=False)
    date = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"))

    def __repr__(self):
        return f"<FoodEntry {self.id}: {self.food_name}>"