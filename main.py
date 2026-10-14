from fastapi import FastAPI
from src.utils.db import Base, engine
from src.tasks.models import TaskModel
from src.tasks.router import task_routes
from src.user.router import user_routes


Base.metadata.create_all(engine)

app = FastAPI(
    title="Task Management App",
    description="This is my Task Management Application"
)
app.include_router(task_routes)
app.include_router(user_routes)
## this is how we connect the database with the FastAPI application. 
@app.get("/")
def home():
    return {"message": "Task Management API is running"}