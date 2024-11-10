import asyncio
import logging
import traceback
from typing import List, TypedDict

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.dto.dto_leader_board import DtoLeadboardData, DtoUpsertLeaderBoard
from app.models.leader_board import LeaderBoard
from app.routes import depends
from app.svc.svc_leaderboard import get_leaderboard

_logger = logging.getLogger("uvicorn")

router = APIRouter()


@router.get("/{quiz_id}", response_model=DtoLeadboardData)
async def api_get_top_leaderboard(
    quiz_id: str,
    leaderboard: depends.LeaderBoardCol,
    user_id: str | None = None,
):
    """Get leaaderboard

    Returns:
        _type_: _description_
    """
    leaderboard_date = await get_leaderboard(quiz_id, leaderboard, user_id=user_id)
    return leaderboard_date


class WsGetLeaderboard(TypedDict):
    limit: int
    user_id: str


@router.websocket("/ws/statistic/{quiz_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    quiz_id: str,
    leaderboard_coll: depends.WsLeaderBoardCol,
    limit: int = 10,
    user_id: str | None = None,
):
    """WS stream leaderboard

    Args:
        websocket (WebSocket): _description_
    """
    await websocket.accept()
    try:
        while True:
            try:
                res = await get_leaderboard(
                    quiz_id,
                    leaderboard_coll,
                    limit=limit,
                    user_id=user_id,
                )
            except Exception as e:
                _logger.error(f"internal service error {e} {traceback.format_exc()}")
            else:
                await websocket.send_json(res.model_dump())
            finally:
                # FIXME Adjust the interval as needed to prevent the frontend send request data too muc
                await asyncio.sleep(2)

    except WebSocketDisconnect:
        _logger.info("client disconnect websocket")
