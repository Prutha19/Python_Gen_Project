from fastapi import FastAPI
from app.controller import user_controller

app = FastAPI(title="My FastAPI Project")

app.include_router(user_controller.router)

@app.get("/")
def root():
    return {"message": "Welcome to FastAPI project!"}
