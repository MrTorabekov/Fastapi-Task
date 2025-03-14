import os
from fastapi import FastAPI
from models import Users
from database import Database
from dotenv import load_dotenv

load_dotenv()

db = Database(
    db_file='fastapi',
    user='postgres',
    password='2008',
    host='localhost',
    port='5432'
)

app = FastAPI()


@app.post("/api/users/")
async def create_user(user: Users):
    if db.check_user(user.username):
        return {"error": "Username already exists"}
    try:
        db.add_user(user.fullname, user.username, user.email, user.password)
        return {"success": True, "data": user}
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.put("/api/users/{user_id}")
async def update_user(user: Users, user_id: int):
    try:
        db.update_user(user_id, user.fullname, user.username, user.email, user.password)
        return {"success": True, "data": user}

    except Exception as e:
        return {"success": False, "error": str(e)}


@app.get("/api/users/")
async def get_users():
    try:
        users = db.get_users()
        all_users = dict(users)
        return {"success": True, "data": all_users}
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.delete("/api/users/{user_id}")
async def delete_user(user_id: int):
    try:
        db.delete_users(user_id)
        return {"success": True, "data": f"{user_id} successfully deleted"}
    except Exception as e:
        return {"success": False, "error": str(e)}