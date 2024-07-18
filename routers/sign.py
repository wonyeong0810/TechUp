from fastapi import APIRouter, Header, HTTPException
from dotenv import load_dotenv
import os
from pymongo import MongoClient
import bcrypt


load_dotenv()


sign = APIRouter(prefix="/sign")
client = MongoClient(os.environ.get("MONGODB_URI"))
db = client["para1"]
print(os.environ.get("MONGO_URI"))

@sign.post("/signup")
def signup(id: str = Header(None), passwd: str = Header(None), level: str = Header(None)):
    print("id:", id, "passwd:", passwd)
    if id is None or passwd is None:
        raise HTTPException(status_code=400, detail="id or pw is None1")
      
    if db['Tusers'].find_one({"id":id}):
        raise HTTPException(status_code=400, detail="id or pw is None2")
    
    hashed_pw = bcrypt.hashpw(passwd.encode('utf-8'), bcrypt.gensalt())
    db['Tusers'].insert_one({"id":id, "pw":hashed_pw, "level":level, "point":0})
    
    return {"status" : 200, "message": "sucess"}

@sign.post("/signin")
def signin(id: str = Header(None), passwd: str = Header(None)):
    if id is None or passwd is None:
        raise HTTPException(status_code=400, detail="id or pw is None")

    user = db['Tusers'].find_one({"id": id})
    if user and bcrypt.checkpw(passwd.encode('utf-8'), user["pw"]):
        return {'status': 200, 'message': 'success'}
    else:
        return {'status': 400, 'message': 'fail'}