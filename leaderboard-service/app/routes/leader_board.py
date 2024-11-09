import asyncio
import logging
from typing import List

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.dto.dto_leader_board import DtoCreateLeaderBoard
from app.models.leader_board import LeaderBoard
from app.routes import depends

_logger = logging.getLogger("uvicorn")

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
    try:
        while True:
            print("[minhne]", f"{quiz_id}")
            res = await leaderboard.find({}, {}).to_list()
            pyres = [LeaderBoard(**rec) for rec in res]

            await websocket.send_json([rec.model_dump() for rec in pyres])
            await asyncio.sleep(5)  # Adjust the interval as needed
    except WebSocketDisconnect:
        _logger.info("client disconnect websocket")
