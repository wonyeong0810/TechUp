# routers/todo.py
from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
from bson import ObjectId
from typing import List, Optional
from datetime import datetime

import os

# MongoDB 클라이언트 설정 (로컬 MongoDB 사용 시)
client = MongoClient(os.environ.get("MONGODB_URI"))
db = client.todo_db
todo_collection = db.get_collection("todos")

router = APIRouter()

def todo_helper(todo) -> dict:
    return {
        "id": str(todo["_id"]),
        "title": todo["title"],
        "description": todo.get("description"),
        "due_date": todo["due_date"],
        "completed": todo["completed"],
    }

@router.post("/", response_model=dict)
async def create_todo_item(title: str, due_date: datetime, description: Optional[str] = None):
    new_todo = {
        "title": title,
        "description": description,
        "due_date": due_date,
        "completed": False
    }
    result = todo_collection.insert_one(new_todo)
    created_todo = todo_collection.find_one({"_id": result.inserted_id})
    return todo_helper(created_todo)

@router.get("/", response_model=List[dict])
async def get_todo_items():
    todos = []
    for todo in todo_collection.find():
        todos.append(todo_helper(todo))
    return todos

@router.get("/{id}", response_model=dict)
async def get_todo_item(id: str):
    todo = todo_collection.find_one({"_id": ObjectId(id)})
    if todo:
        return todo_helper(todo)
    else:
        raise HTTPException(status_code=404, detail="Todo item not found")

@router.put("/{id}", response_model=dict)
async def update_todo_item(id: str, title: Optional[str] = None, due_date: Optional[datetime] = None, description: Optional[str] = None, completed: Optional[bool] = None):
    update_data = {}
    if title is not None:
        update_data["title"] = title
    if due_date is not None:
        update_data["due_date"] = due_date
    if description is not None:
        update_data["description"] = description
    if completed is not None:
        update_data["completed"] = completed
    
    updated_todo = todo_collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": update_data},
        return_document=True
    )
    if updated_todo:
        return todo_helper(updated_todo)
    else:
        raise HTTPException(status_code=404, detail="Todo item not found")

@router.delete("/{id}", response_model=dict)
async def delete_todo_item(id: str):
    result = todo_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count:
        return {"message": "Todo item deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Todo item not found")
