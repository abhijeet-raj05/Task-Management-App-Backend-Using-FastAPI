from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from src.utils.db import Base

# Base is responsible to connecet my table with the database.

class TaskModel(Base):
    __tablename__ = "users_tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    is_completed = Column(Boolean, default=False)

    user_id = Column(Integer, ForeignKey("user_table.id", ondelete="CASCADE"))
    