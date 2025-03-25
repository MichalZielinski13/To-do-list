from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId

client = MongoClient("mongodb://localhost:27017/")
db = client["todolist"]

collection = db["items"]

app = FastAPI()

items = []

class Item(BaseModel):
    item: str

@app.get("/")
def show_title():
    title = 'To do list'
    return title

@app.post("/items")
def add_item(item: Item):
    result = collection.insert_one(item)
    if not result.inserted_id:
        raise HTTPException(status_code=500, detail="Failed to add item")
    return {"message": f'Item {result.inserted_id} was added successfully'}

@app.get("/items/{item_id}")
def get_item(item_id: str):
    item = collection.find_one({"_id": ObjectId(item_id)})
    if item:
        return {f'This is your item: {item}'}

@app.put("/items/{item_id}")
def change_item(item_id: str, item: Item):
    result = collection.update_one({"_id": ObjectId(item_id)}, {"$set": item})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {f'This item:  "id": ${item_id}, "item": {item.item} was modified'}

@app.delete("/items/{item_id}")
def delete_item(item_id: str):
    result = collection.delete_one({"_id": ObjectId(item_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": f'Item "{item_id}" deleted successfully'}