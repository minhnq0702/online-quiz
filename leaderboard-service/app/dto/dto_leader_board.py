from typing import List

from pydantic import BaseModel

from app.models.leader_board import LeaderBoard


class DtoUpsertLeaderBoard(BaseModel):
    """
    DTO for creating a new leaderboard entry
    """
    quiz_id: str
    user_id: str
    score: float


class DtoUserRank(BaseModel):
    rank: int | None
    score: float | None


class DtoLeadboardData(BaseModel):
    top_ranks: List[LeaderBoard]
    user_rank: DtoUserRank | None
