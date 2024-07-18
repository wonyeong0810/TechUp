# routers/sign.py
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from pymongo import MongoClient
import bcrypt

load_dotenv()

class UserSignup(BaseModel):
    id: str
    passwd: str
    level: str

class UserSignin(BaseModel):
    id: str
    passwd: str

router = APIRouter()

client = MongoClient(os.environ.get("MONGODB_URI"))
db = client["para1"]

@router.post("/signup")
def signup(user: UserSignup):
    if db['Tusers'].find_one({"id": user.id}):
        raise HTTPException(status_code=400, detail="User already exists")
    
    hashed_pw = bcrypt.hashpw(user.passwd.encode('utf-8'), bcrypt.gensalt())
    db['Tusers'].insert_one({"id": user.id, "pw": hashed_pw, "level": user.level, "point": 0})
    
    return {"status": 200, "message": "Success"}

@router.post("/signin")
def signin(user: UserSignin):
    stored_user = db['Tusers'].find_one({"id": user.id})
    if stored_user and bcrypt.checkpw(user.passwd.encode('utf-8'), stored_user["pw"]):
        return {'status': 200, 'message': 'Success'}
    else:
        raise HTTPException(status_code=400, detail="Invalid credentials")
