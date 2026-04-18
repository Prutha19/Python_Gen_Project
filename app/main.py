from fastapi import FastAPI
from .controller import file_controller
from .controller import AuthController
from .controller import product_controller
from .database import engine, get_db_session
from .models import Base, User, Role, Product
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles
from .controller import TestRideController

Base.metadata.create_all(bind=engine)

def seed_roles():
    db: Session = get_db_session()
    try:
        if db.query(Role).first() is None:
            admin_role = Role(name="ROLE_ADMIN")
            user_role = Role(name="ROLE_USER")
            db.add(admin_role)
            db.add(user_role)
            db.commit()
            print("Roles seeded successfully")
    except Exception as e:
        print(f"Error seeding roles: {e}")
    finally:
        db.close()

seed_roles()

app = FastAPI(title="My FastAPI Project")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/ProductImage", StaticFiles(directory="ProductImage"), name="ProductImage")

app.include_router(file_controller.router)
app.include_router(AuthController.router)
app.include_router(product_controller.router)
app.include_router(TestRideController.router)
@app.get("/")
def root():
    return {"message": "Welcome to FastAPI project!"}
