import asyncio
from typing import List

from fastapi import APIRouter, WebSocket

from app.dto.dto_leader_board import DtoCreateLeaderBoard
from app.models.leader_board import LeaderBoard
from app.routes import depends

router = APIRouter()


@router.post("/", response_model=LeaderBoard)
async def create_leaderboard_entry(
    entry: DtoCreateLeaderBoard,
    leaderboard: depends.LeaderBoardCol,
):
    """
    Create a new leaderboard entry in the database.

    Returns:
        LeaderboardEntry: The created leaderboard entry.
    """
    new_entry = await leaderboard.insert_one(entry.model_dump())
    create_entry = await leaderboard.find_one({
        "_id": new_entry.inserted_id,
    })
    return create_entry


@router.get("/", response_model=List[LeaderBoard])
async def get_leaderboard(
    leaderboard: depends.LeaderBoardCol,
):
    """Get leaaderboard

    Returns:
        _type_: _description_
    """
    entries = await leaderboard.find({}, {}).to_list()
    return entries


@router.websocket("/ws/statistic/{quiz_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    quiz_id: int,
    leaderboard: depends.WsLeaderBoardCol,
):
    """WS stream leaderboard

    Args:
        websocket (WebSocket): _description_
    """
    await websocket.accept()
    while True:
        print("[minhne]", f"{quiz_id}")
        res = await leaderboard.find({}, {"_id": 0, "score": 1, "username": 1}).to_list()
        await websocket.send_json(res)
        await asyncio.sleep(5)  # Adjust the interval as needed
