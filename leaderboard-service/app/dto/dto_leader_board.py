from pydantic import BaseModel


class DtoCreateLeaderBoard(BaseModel):
    """
    DTO for creating a new leaderboard entry
    """
    quiz_id: int
    username: str
    score: float
