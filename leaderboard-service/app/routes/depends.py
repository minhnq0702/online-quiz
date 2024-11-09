from typing import Annotated

from fastapi import Depends, Request, WebSocket
from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase


async def get_leadrboard_collection(req: Request) -> AsyncIOMotorCollection:
    """
    Get leaderboard collection
    """
    db: AsyncIOMotorDatabase = req.app.state.mongodb
    leaderboard: AsyncIOMotorCollection = db.get_collection("leaderboard")
    return leaderboard


async def ws_get_leaderboard_collection(ws: WebSocket) -> AsyncIOMotorCollection:
    """
    Get leaderboard collection
    """
    db: AsyncIOMotorDatabase = ws.app.state.mongodb
    leaderboard: AsyncIOMotorCollection = db.get_collection("leaderboard")
    return leaderboard


LeaderBoardCol = Annotated[AsyncIOMotorCollection, Depends(get_leadrboard_collection)]
WsLeaderBoardCol = Annotated[AsyncIOMotorCollection, Depends(ws_get_leaderboard_collection)]
