import asyncio
import logging
from typing import List

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Request, WebSocket
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from pymongo import MongoClient

from app.repo.db import close_db_client, init_db_client

_logger = logging.getLogger("uvicorn")

load_dotenv()


async def lifespan(_app: FastAPI):
    await init_db_client(_app)
    yield
    close_db_client(_app)

app = FastAPI(
    lifespan=lifespan,
)


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


@app.websocket("/ws/leaderboard/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        # entries = list(collection.find({}, {"_id": 0})) # TODO get from mongo
        entries = [
            {"username": "user1", "score": 100},
            {"username": "user2", "score": 95},
            {"username": "user3", "score": 90}
        ]
        await websocket.send_json(entries)
        await asyncio.sleep(5)  # Adjust the interval as needed
