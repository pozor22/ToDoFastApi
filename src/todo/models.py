from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True)
    name = Column(String(60), nullable=False)
    description = Column(String)
    is_done = Column(Boolean, default=False)
    user_id = Column(ForeignKey('user.id'))
