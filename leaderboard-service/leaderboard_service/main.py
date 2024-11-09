from typing import List

from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient

app = FastAPI()

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["quiz_db"]
collection = db["leaderboard"]

class LeaderboardEntry(BaseModel):
    username: str
    score: int

@app.post("/leaderboard/", response_model=LeaderboardEntry)
async def create_leaderboard_entry(entry: LeaderboardEntry):
    collection.insert_one(entry.dict())
    return entry

@app.get("/leaderboard/", response_model=List[LeaderboardEntry])
async def get_leaderboard():
    entries = list(collection.find({}, {"_id": 0}))
    return entries