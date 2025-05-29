
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float
from sqlalchemy.orm import relationship,Session
from health_cli.db.database import Base
from sqlalchemy.exc import IntegrityError



class Goal(Base):
    __tablename__ = 'goals'
    id = Column(Integer, primary_key=True)
    daily_calories = Column(Integer)
    weekly_calories = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)
    description = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    target = Column(Float, nullable=False)
    user = relationship("User", back_populates="goals")




# CREATE
def create_goal(db: Session, user_id: int, daily_calories: int, weekly_calories: int, description: str, target: float, date: date):
    try:
        goal = Goal(
            user_id=user_id,
            daily_calories=daily_calories,
            weekly_calories=weekly_calories,
            description=description,
            target=target,
            date=date
        )
        db.add(goal)
        db.commit()
        db.refresh(goal)
        return goal
    except IntegrityError:
        db.rollback()
        raise ValueError("Goal with this user_id already exists")

# READ
def get_goal_by_user_id(db: Session, user_id: int):
    return db.query(Goal).filter(Goal.user_id == user_id).first()

def get_goal_by_id(db: Session, goal_id: int):
    return db.query(Goal).filter(Goal.id == goal_id).first()

# UPDATE
def update_goal(db: Session, goal_id: int, updated_data: dict):
    goal = db.query(Goal).filter(Goal.id == goal_id).first()
    if goal:
        for key, value in updated_data.items():
            if hasattr(goal, key):
                setattr(goal, key, value)
        db.commit()
        db.refresh(goal)
    return goal

# DELETE
def delete_goal(db: Session, goal_id: int):
    goal = db.query(Goal).filter(Goal.id == goal_id).first()
    if goal:
        db.delete(goal)
        db.commit()
    return goal